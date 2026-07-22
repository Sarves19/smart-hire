"""
Login History Repository

Data access layer for login history records.
"""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.login_history import LoginHistory, LoginStatus

logger = logging.getLogger("smart_hire.repositories")


class LoginHistoryRepository:
    """
    Repository for login history operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, record: LoginHistory) -> LoginHistory:
        """Create a new login history record."""
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        logger.info(
            "Login recorded: user_id=%s status=%s ip=%s",
            record.user_id,
            record.status.value,
            record.ip_address,
        )
        return record

    def get_recent_by_user(
        self,
        user_id: int,
        limit: int = 10,
    ) -> list[LoginHistory]:
        """Get recent login records for a user."""
        records = (
            self.db.query(LoginHistory)
            .filter(LoginHistory.user_id == user_id)
            .order_by(desc(LoginHistory.created_at))
            .limit(limit)
            .all()
        )
        return records

    def get_last_successful(self, user_id: int) -> LoginHistory | None:
        """Get the last successful login for a user."""
        record = (
            self.db.query(LoginHistory)
            .filter(
                LoginHistory.user_id == user_id,
                LoginHistory.status == LoginStatus.SUCCESS,
            )
            .order_by(desc(LoginHistory.created_at))
            .first()
        )
        return record

    def get_failed_attempts(
        self,
        user_id: int,
        minutes: int = 30,
    ) -> list[LoginHistory]:
        """Get failed login attempts in the last N minutes."""
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
        records = (
            self.db.query(LoginHistory)
            .filter(
                LoginHistory.user_id == user_id,
                LoginHistory.status != LoginStatus.SUCCESS,
                LoginHistory.created_at >= cutoff,
            )
            .order_by(desc(LoginHistory.created_at))
            .all()
        )
        return records

    def get_by_ip_address(
        self,
        user_id: int,
        ip_address: str,
    ) -> list[LoginHistory]:
        """Get login attempts from a specific IP address."""
        records = (
            self.db.query(LoginHistory)
            .filter(
                LoginHistory.user_id == user_id,
                LoginHistory.ip_address == ip_address,
            )
            .order_by(desc(LoginHistory.created_at))
            .all()
        )
        return records

    def mark_notification_sent(self, record: LoginHistory) -> LoginHistory:
        """Mark that a login notification email was sent."""
        record.notification_sent = True
        self.db.commit()
        self.db.refresh(record)
        return record

    def update_status(
        self,
        record: LoginHistory,
        status: LoginStatus,
        failure_reason: str | None = None,
    ) -> LoginHistory:
        """Update the status of a login attempt."""
        record.status = status
        record.failure_reason = failure_reason
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_suspicious_logins(
        self,
        user_id: int,
        hours: int = 24,
    ) -> list[LoginHistory]:
        """Get logins from new locations/devices in the last N hours."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        # Get all successful logins in timeframe
        recent_logins = (
            self.db.query(LoginHistory)
            .filter(
                LoginHistory.user_id == user_id,
                LoginHistory.status == LoginStatus.SUCCESS,
                LoginHistory.created_at >= cutoff,
                LoginHistory.is_trusted_device == False,
            )
            .order_by(desc(LoginHistory.created_at))
            .all()
        )
        return recent_logins

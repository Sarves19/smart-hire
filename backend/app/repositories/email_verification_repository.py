"""
Email Verification Repository

Handles all database operations for OTP / email verification
records.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.email_verification import EmailVerification, OtpPurpose


class EmailVerificationRepository:
    """
    Repository responsible for EmailVerification (OTP) rows.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, record: EmailVerification) -> EmailVerification:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    # =====================================================
    # READ
    # =====================================================

    def get_latest_active(
        self,
        user_id: int,
        purpose: OtpPurpose,
    ) -> Optional[EmailVerification]:
        """
        Return the most recent, unused OTP for this user and
        purpose (used and expired ones are ignored).
        """

        stmt = (
            select(EmailVerification)
            .where(
                EmailVerification.user_id == user_id,
                EmailVerification.purpose == purpose,
                EmailVerification.is_used.is_(False),
            )
            .order_by(EmailVerification.created_at.desc())
        )

        result = self.db.execute(stmt)

        return result.scalars().first()

    # =====================================================
    # UPDATE
    # =====================================================

    def invalidate_active(
        self,
        user_id: int,
        purpose: OtpPurpose,
    ) -> None:
        """
        Mark any existing unused OTPs for this user/purpose as
        used, so only the newest one that gets issued is ever
        valid (prevents an old, leaked OTP from still working).
        """

        stmt = (
            update(EmailVerification)
            .where(
                EmailVerification.user_id == user_id,
                EmailVerification.purpose == purpose,
                EmailVerification.is_used.is_(False),
            )
            .values(is_used=True)
        )

        self.db.execute(stmt)
        self.db.commit()

    def replace_active(self, record: EmailVerification) -> EmailVerification:
        """Atomically invalidate old OTPs and persist the replacement."""
        try:
            # Invalidate previous unused codes
            stmt = (
                update(EmailVerification)
                .where(
                    EmailVerification.user_id == record.user_id,
                    EmailVerification.purpose == record.purpose,
                    EmailVerification.is_used.is_(False),
                )
                .values(is_used=True)
            )
            self.db.execute(stmt)
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            return record
        except Exception:
            self.db.rollback()
            raise

    def save(self, record: EmailVerification) -> EmailVerification:
        self.db.commit()
        self.db.refresh(record)
        return record

    # =====================================================
    # HOUSEKEEPING
    # =====================================================

    def is_expired(self, record: EmailVerification) -> bool:
        expires_at = record.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        return datetime.now(timezone.utc) > expires_at

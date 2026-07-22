"""
Notification Repository

Handles all database operations related to notifications.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification


class NotificationRepository:
    """
    Repository responsible for notification operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        notification: Notification,
    ) -> Notification:
        """
        Create a notification.
        """

        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)

        return notification

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(
        self,
        notification_id: int,
    ) -> Optional[Notification]:
        """
        Get notification by ID.
        """

        stmt = select(Notification).where(
            Notification.id == notification_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_user_notifications(
        self,
        user_id: int,
    ) -> list[Notification]:
        """
        Return all notifications for a user.
        """

        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    def list_notifications(self) -> list[Notification]:
        """
        Return all notifications.
        """

        stmt = select(Notification)

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        notification: Notification,
    ) -> Notification:
        """
        Update notification.
        """

        self.db.commit()
        self.db.refresh(notification)

        return notification

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        notification: Notification,
    ) -> None:
        """
        Delete notification.
        """

        self.db.delete(notification)
        self.db.commit()
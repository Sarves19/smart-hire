"""
Notification Service

Contains business logic for notification management.
"""

from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.user import User
from app.repositories.notification_repository import (
    NotificationRepository,
)
from app.repositories.user_repository import UserRepository
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)


class NotificationService:
    """
    Handles notification business logic.
    """

    def __init__(self, db: Session):
        self.notification_repository = NotificationRepository(db)
        self.user_repository = UserRepository(db)

    # =====================================================
    # CREATE NOTIFICATION
    # =====================================================

    def create_notification(
        self,
        request: NotificationCreate,
    ) -> Notification:
        """
        Create a notification.
        """

        user = self.user_repository.get_by_id(
            request.user_id
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        notification = Notification(
            user_id=request.user_id,
            title=request.title,
            message=request.message,
            notification_type=request.notification_type,
            is_read=False,
        )

        return self.notification_repository.create(
            notification
        )

    # =====================================================
    # GET NOTIFICATION
    # =====================================================

    def get_notification(
        self,
        notification_id: int,
        user: User,
    ) -> Notification:

        notification = (
            self.notification_repository.get_by_id(
                notification_id
            )
        )

        if notification is None:
            raise ValueError(
                "Notification not found."
            )

        self._assert_can_access(notification, user)
        return notification

    # =====================================================
    # LIST NOTIFICATIONS
    # =====================================================

    def list_notifications(
        self,
        user: User,
    ) -> list[Notification]:

        if user.role.value == "ADMIN":
            return self.notification_repository.list_notifications()
        return self.notification_repository.get_user_notifications(user.id)

    # =====================================================
    # USER NOTIFICATIONS
    # =====================================================

    def get_user_notifications(
        self,
        user_id: int,
        user: User,
    ) -> list[Notification]:

        if user.role.value != "ADMIN" and user.id != user_id:
            raise ValueError("You do not have permission to access these notifications.")
        return (
            self.notification_repository.get_user_notifications(
                user_id
            )
        )

    # =====================================================
    # MARK AS READ
    # =====================================================

    def update_notification(
        self,
        notification_id: int,
        request: NotificationUpdate,
        user: User,
    ) -> Notification:

        notification = (
            self.notification_repository.get_by_id(
                notification_id
            )
        )

        if notification is None:
            raise ValueError(
                "Notification not found."
            )

        self._assert_can_access(notification, user)

        notification.is_read = request.is_read

        return self.notification_repository.update(
            notification
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_notification(
        self,
        notification_id: int,
        user: User,
    ) -> None:

        notification = (
            self.notification_repository.get_by_id(
                notification_id
            )
        )

        if notification is None:
            raise ValueError(
                "Notification not found."
            )

        self._assert_can_access(notification, user)

        self.notification_repository.delete(
            notification
        )

    @staticmethod
    def _assert_can_access(notification: Notification, user: User) -> None:
        if user.role.value != "ADMIN" and notification.user_id != user.id:
            raise ValueError("You do not have permission to access this notification.")

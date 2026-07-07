"""
User Service

Contains the business logic for user management.
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdateRequest


class UserService:
    """
    Handles user-related business logic.
    """

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    # =====================================================
    # READ
    # =====================================================

    def get_current_user(
        self,
        user: User,
    ) -> User:
        """
        Returns the currently authenticated user.
        """
        return user

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """
        Returns a user by ID.
        """
        return self.user_repository.get_by_id(user_id)

    def list_users(self) -> list[User]:
        """
        Returns all users.
        """
        return self.user_repository.list_users()

    # =====================================================
    # UPDATE
    # =====================================================

    def update_user(
        self,
        user: User,
        request: UserUpdateRequest,
    ) -> User:
        """
        Updates user profile.
        """

        if request.first_name is not None:
            user.first_name = request.first_name

        if request.last_name is not None:
            user.last_name = request.last_name

        if request.phone_number is not None:
            user.phone_number = request.phone_number

        return self.user_repository.update(user)
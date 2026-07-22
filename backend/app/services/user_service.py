"""
User Service

Contains the business logic for user management.
"""

from sqlalchemy.orm import Session

from app.core.security import password_manager
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import PasswordChangeRequest, UserUpdateRequest


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

    def list_user_page(
        self,
        page: int,
        page_size: int,
        search: str | None,
        role: UserRole | None,
        is_active: bool | None,
    ) -> tuple[list[User], int]:
        return self.user_repository.list_page(page, page_size, search, role, is_active)

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
            existing_user = self.user_repository.get_by_phone(request.phone_number)
            if existing_user is not None and existing_user.id != user.id:
                raise ValueError("Phone number already exists.")
            user.phone_number = request.phone_number

        return self.user_repository.update(user)

    def change_password(self, user: User, request: PasswordChangeRequest) -> None:
        """Verify the existing Argon2 hash before replacing it."""
        if not password_manager.verify_password(request.current_password, user.password_hash):
            raise ValueError("Current password is incorrect.")
        user.password_hash = password_manager.hash_password(request.new_password)
        self.user_repository.update(user)

    def set_account_status(self, target_user: User, is_active: bool, actor: User) -> User:
        """Administrators may not deactivate their own account."""
        if target_user.id == actor.id and not is_active:
            raise ValueError("You cannot deactivate your own account.")
        target_user.is_active = is_active
        return self.user_repository.update(target_user)

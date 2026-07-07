"""
User Repository

Handles all database operations related to users.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Repository responsible for all User database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, user: User) -> User:
        """
        Create a new user.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        """
        stmt = select(User).where(User.id == user_id)

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        """
        stmt = select(User).where(User.email == email)

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_phone(self, phone_number: str) -> Optional[User]:
        """
        Get user by phone number.
        """
        stmt = select(User).where(User.phone_number == phone_number)

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def list_users(self) -> list[User]:
        """
        Return all users.
        """
        stmt = select(User)

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    # =====================================================
    # VALIDATION
    # =====================================================

    def email_exists(self, email: str) -> bool:
        """
        Check whether an email already exists.
        """
        return self.get_by_email(email) is not None

    def phone_exists(self, phone_number: str) -> bool:
        """
        Check whether a phone number already exists.
        """
        return self.get_by_phone(phone_number) is not None

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, user: User) -> User:
        """
        Update an existing user.
        """
        self.db.commit()
        self.db.refresh(user)
        return user

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, user: User) -> None:
        """
        Delete a user.
        """
        self.db.delete(user)
        self.db.commit()
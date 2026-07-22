"""
User Repository

Handles all database operations related to users.
"""

import logging
from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User, UserRole

logger = logging.getLogger("smart_hire.user_repository")


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
        logger.info("create() adding user with email=%s phone=%s", user.email, user.phone_number)
        self.db.add(user)
        try:
            logger.info("create() committing transaction")
            self.db.commit()
            logger.info("create() commit successful, refreshing user object")
            self.db.refresh(user)
            logger.info("create() user created with id=%s", user.id)
            return user
        except IntegrityError as exc:
            logger.exception("create() IntegrityError during commit: %s", exc)
            self.db.rollback()
            logger.info("create() transaction rolled back")
            raise ValueError("Email or phone number already exists.") from exc
        except Exception as exc:
            logger.exception("create() unexpected exception: %s", exc)
            self.db.rollback()
            logger.info("create() transaction rolled back due to exception")
            raise

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

    def list_page(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[User], int]:
        """Return a stable, filtered admin page and its total count."""
        filters = []
        if search:
            term = f"%{search.strip().lower()}%"
            filters.append(or_(
                func.lower(User.first_name).like(term),
                func.lower(User.last_name).like(term),
                func.lower(User.email).like(term),
                User.phone_number.like(term),
            ))
        if role is not None:
            filters.append(User.role == role)
        if is_active is not None:
            filters.append(User.is_active.is_(is_active))

        stmt = select(User).where(*filters).order_by(User.id.desc())
        total = self.db.scalar(select(func.count()).select_from(User).where(*filters)) or 0
        users = self.db.execute(
            stmt.offset((page - 1) * page_size).limit(page_size)
        ).scalars().all()
        return list(users), total

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
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise ValueError("Email or phone number already exists.") from exc

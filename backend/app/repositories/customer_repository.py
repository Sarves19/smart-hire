"""
Customer Profile Repository

Handles all database operations related to customer profiles.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer_profile import CustomerProfile


class CustomerRepository:
    """
    Repository responsible for Customer Profile operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        profile: CustomerProfile,
    ) -> CustomerProfile:
        """
        Create a customer profile.
        """

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile

    # =====================================================
    # READ
    # =====================================================

    def get_by_user_id(
        self,
        user_id: int,
    ) -> Optional[CustomerProfile]:
        """
        Get customer profile by user ID.
        """

        stmt = select(CustomerProfile).where(
            CustomerProfile.user_id == user_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        profile: CustomerProfile,
    ) -> CustomerProfile:
        """
        Update customer profile.
        """

        self.db.commit()
        self.db.refresh(profile)

        return profile

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        profile: CustomerProfile,
    ) -> None:
        """
        Delete customer profile.
        """

        self.db.delete(profile)
        self.db.commit()
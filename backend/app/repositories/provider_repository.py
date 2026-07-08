"""
Provider Profile Repository

Handles all database operations related to provider profiles.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.provider_profile import ProviderProfile


class ProviderRepository:
    """
    Repository responsible for Provider Profile operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        profile: ProviderProfile,
    ) -> ProviderProfile:
        """
        Create a provider profile.
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
    ) -> Optional[ProviderProfile]:
        """
        Get provider profile by user ID.
        """

        stmt = select(ProviderProfile).where(
            ProviderProfile.user_id == user_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        profile: ProviderProfile,
    ) -> ProviderProfile:
        """
        Update provider profile.
        """

        self.db.commit()
        self.db.refresh(profile)

        return profile

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        profile: ProviderProfile,
    ) -> None:
        """
        Delete provider profile.
        """

        self.db.delete(profile)
        self.db.commit()
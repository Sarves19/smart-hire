"""
Recommendation Repository

Provides data for AI recommendations.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.provider_profile import ProviderProfile
from app.models.service import Service


class RecommendationRepository:
    """
    Repository responsible for fetching recommendation data.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # Categories
    # =====================================================

    def get_all_categories(self):
        """
        Get all service categories.
        """

        stmt = select(Category)

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    # =====================================================
    # Services
    # =====================================================

    def get_all_services(self):
        """
        Get all services.
        """

        stmt = select(Service)

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    # =====================================================
    # Providers
    # =====================================================

    def get_all_providers(self):
        """
        Get all service providers.
        """

        stmt = select(ProviderProfile)

        result = self.db.execute(stmt)

        return list(result.scalars().all())
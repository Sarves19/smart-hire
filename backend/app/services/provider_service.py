"""
Provider Profile Service

Contains business logic for provider profile management.
"""

from sqlalchemy.orm import Session

from app.models.provider_profile import ProviderProfile
from app.models.user import User
from app.repositories.provider_repository import ProviderRepository
from app.schemas.provider import (
    ProviderProfileCreate,
    ProviderProfileUpdate,
)


class ProviderService:
    """
    Handles provider profile business logic.
    """

    def __init__(self, db: Session):
        self.repository = ProviderRepository(db)

    # =====================================================
    # CREATE
    # =====================================================

    def create_profile(
        self,
        user: User,
        request: ProviderProfileCreate,
    ) -> ProviderProfile:
        """
        Create a provider profile.
        """

        existing_profile = self.repository.get_by_user_id(user.id)

        if existing_profile:
            raise ValueError("Provider profile already exists.")

        profile = ProviderProfile(
            user_id=user.id,
            business_name=request.business_name,
            business_registration_number=request.business_registration_number,
            description=request.description,
            years_of_experience=request.years_of_experience,
            business_address=request.business_address,
            city=request.city,
            district=request.district,
            service_radius_km=request.service_radius_km,
            business_logo=request.business_logo,
            is_verified=False,
        )

        return self.repository.create(profile)

    # =====================================================
    # READ
    # =====================================================

    def get_profile(
        self,
        user: User,
    ) -> ProviderProfile:
        """
        Get provider profile.
        """

        profile = self.repository.get_by_user_id(user.id)

        if profile is None:
            raise ValueError("Provider profile not found.")

        return profile

    # =====================================================
    # UPDATE
    # =====================================================

    def update_profile(
        self,
        user: User,
        request: ProviderProfileUpdate,
    ) -> ProviderProfile:
        """
        Update provider profile.
        """

        profile = self.repository.get_by_user_id(user.id)

        if profile is None:
            raise ValueError("Provider profile not found.")

        if request.business_name is not None:
            profile.business_name = request.business_name

        if request.business_registration_number is not None:
            profile.business_registration_number = (
                request.business_registration_number
            )

        if request.description is not None:
            profile.description = request.description

        if request.years_of_experience is not None:
            profile.years_of_experience = request.years_of_experience

        if request.business_address is not None:
            profile.business_address = request.business_address

        if request.city is not None:
            profile.city = request.city

        if request.district is not None:
            profile.district = request.district

        if request.service_radius_km is not None:
            profile.service_radius_km = request.service_radius_km

        if request.business_logo is not None:
            profile.business_logo = request.business_logo

        return self.repository.update(profile)
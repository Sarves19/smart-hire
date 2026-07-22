"""
Customer Profile Service

Contains business logic for customer profile management.
"""

from sqlalchemy.orm import Session

from app.models.customer_profile import CustomerProfile
from app.models.user import User
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import (
    CustomerProfileCreate,
    CustomerProfileUpdate,
)


class CustomerService:
    """
    Handles customer profile business logic.
    """

    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    # =====================================================
    # CREATE
    # =====================================================

    def create_profile(
        self,
        user: User,
        request: CustomerProfileCreate,
    ) -> CustomerProfile:
        """
        Create a customer profile.
        """

        existing_profile = self.repository.get_by_user_id(user.id)

        if existing_profile:
            raise ValueError("Customer profile already exists.")

        profile = CustomerProfile(
            user_id=user.id,
            profile_image=request.profile_image,
            address=request.address,
            city=request.city,
            district=request.district,
        )

        return self.repository.create(profile)

    # =====================================================
    # READ
    # =====================================================

    def get_profile(
        self,
        user: User,
    ) -> CustomerProfile:
        """
        Get customer profile.
        """

        profile = self.repository.get_by_user_id(user.id)

        if profile is None:
            raise ValueError("Customer profile not found.")

        return profile

    # =====================================================
    # UPDATE
    # =====================================================

    def update_profile(
        self,
        user: User,
        request: CustomerProfileUpdate,
    ) -> CustomerProfile:
        """
        Update customer profile.
        """

        profile = self.repository.get_by_user_id(user.id)

        if profile is None:
            raise ValueError("Customer profile not found.")

        if request.profile_image is not None:
            profile.profile_image = request.profile_image

        if request.address is not None:
            profile.address = request.address

        if request.city is not None:
            profile.city = request.city

        if request.district is not None:
            profile.district = request.district

        return self.repository.update(profile)
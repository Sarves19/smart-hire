"""
Service Service

Contains business logic for service management.
"""

from sqlalchemy.orm import Session

from app.models.provider_profile import ProviderProfile
from app.models.service import Service
from app.models.user import User
from app.repositories.provider_repository import ProviderRepository
from app.repositories.service_repository import ServiceRepository
from app.schemas.service import (
    ServiceCreate,
    ServiceUpdate,
)


class ServiceService:
    """
    Handles service business logic.
    """

    def __init__(self, db: Session):
        self.service_repository = ServiceRepository(db)
        self.provider_repository = ProviderRepository(db)

    # =====================================================
    # CREATE
    # =====================================================

    def create_service(
        self,
        user: User,
        request: ServiceCreate,
    ) -> Service:
        """
        Create a new service for the logged-in provider.
        """

        provider: ProviderProfile | None = (
            self.provider_repository.get_by_user_id(user.id)
        )

        if provider is None:
            raise ValueError(
                "Provider profile not found."
            )

        service = Service(
            provider_id=provider.id,
            category_id=request.category_id,
            title=request.title,
            description=request.description,
            price=request.price,
            duration_minutes=request.duration_minutes,
            service_location=request.service_location,
            image_url=request.image_url,
            is_available=True,
        )

        return self.service_repository.create(service)

    # =====================================================
    # READ
    # =====================================================

    def get_service(
        self,
        service_id: int,
    ) -> Service:
        """
        Get service by ID.
        """

        service = self.service_repository.get_by_id(
            service_id
        )

        if service is None:
            raise ValueError("Service not found.")

        return service

    def list_services(self) -> list[Service]:
        """
        List all services.
        """

        return self.service_repository.list_services()

    # =====================================================
    # UPDATE
    # =====================================================

    def update_service(
        self,
        service_id: int,
        request: ServiceUpdate,
    ) -> Service:
        """
        Update a service.
        """

        service = self.service_repository.get_by_id(
            service_id
        )

        if service is None:
            raise ValueError("Service not found.")

        if request.category_id is not None:
            service.category_id = request.category_id

        if request.title is not None:
            service.title = request.title

        if request.description is not None:
            service.description = request.description

        if request.price is not None:
            service.price = request.price

        if request.duration_minutes is not None:
            service.duration_minutes = request.duration_minutes

        if request.service_location is not None:
            service.service_location = request.service_location

        if request.image_url is not None:
            service.image_url = request.image_url

        if request.is_available is not None:
            service.is_available = request.is_available

        return self.service_repository.update(service)

    # =====================================================
    # DELETE
    # =====================================================

    def delete_service(
        self,
        service_id: int,
    ) -> None:
        """
        Delete a service.
        """

        service = self.service_repository.get_by_id(
            service_id
        )

        if service is None:
            raise ValueError("Service not found.")

        self.service_repository.delete(service)
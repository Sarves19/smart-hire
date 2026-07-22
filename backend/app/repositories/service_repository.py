"""
Service Repository

Handles all database operations related to services.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service import Service


class ServiceRepository:
    """
    Repository responsible for Service operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        service: Service,
    ) -> Service:
        """
        Create a service.
        """

        self.db.add(service)
        self.db.commit()
        self.db.refresh(service)

        return service

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(
        self,
        service_id: int,
    ) -> Optional[Service]:
        """
        Get service by ID.
        """

        stmt = select(Service).where(
            Service.id == service_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_provider(
        self,
        provider_id: int,
    ) -> list[Service]:
        """
        Get all services belonging to a provider.
        """

        stmt = select(Service).where(
            Service.provider_id == provider_id
        )

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    def list_services(self) -> list[Service]:
        """
        Return all services.
        """

        stmt = select(Service)

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        service: Service,
    ) -> Service:
        """
        Update service.
        """

        self.db.commit()
        self.db.refresh(service)

        return service

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        service: Service,
    ) -> None:
        """
        Delete service.
        """

        self.db.delete(service)
        self.db.commit()
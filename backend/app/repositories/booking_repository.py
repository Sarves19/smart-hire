"""
Booking Repository

Handles all database operations related to bookings.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.service import Service


class BookingRepository:
    """
    Repository responsible for booking operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        booking: Booking,
    ) -> Booking:
        """
        Create a new booking.
        """

        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)

        return booking

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(
        self,
        booking_id: int,
    ) -> Optional[Booking]:
        """
        Get booking by ID.
        """

        stmt = select(Booking).where(
            Booking.id == booking_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_customer_bookings(
        self,
        customer_id: int,
    ) -> list[Booking]:
        """
        Return bookings of a customer.
        """

        stmt = select(Booking).where(
            Booking.customer_id == customer_id
        )

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    def get_provider_bookings(
        self,
        provider_id: int,
    ) -> list[Booking]:
        """
        Return bookings of a provider (joined through the
        booked service, since bookings don't store provider_id
        directly).
        """

        stmt = (
            select(Booking)
            .join(Service, Booking.service_id == Service.id)
            .where(Service.provider_id == provider_id)
        )

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    def list_bookings(self) -> list[Booking]:
        """
        Return all bookings.
        """

        stmt = select(Booking)

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        booking: Booking,
    ) -> Booking:
        """
        Update a booking.
        """

        self.db.commit()
        self.db.refresh(booking)

        return booking

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        booking: Booking,
    ) -> None:
        """
        Delete a booking.
        """

        self.db.delete(booking)
        self.db.commit()
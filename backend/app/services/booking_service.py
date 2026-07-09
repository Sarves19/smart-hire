"""
Booking Service

Contains business logic for booking management.
"""

from sqlalchemy.orm import Session

from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.repositories.booking_repository import BookingRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.provider_repository import ProviderRepository
from app.repositories.service_repository import ServiceRepository
from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
)


class BookingService:
    """
    Handles booking business logic.
    """

    def __init__(self, db: Session):
        self.booking_repository = BookingRepository(db)
        self.customer_repository = CustomerRepository(db)
        self.provider_repository = ProviderRepository(db)
        self.service_repository = ServiceRepository(db)

    # =====================================================
    # CREATE BOOKING
    # =====================================================

    def create_booking(
        self,
        user: User,
        request: BookingCreate,
    ) -> Booking:
        """
        Create a booking.
        """

        customer = self.customer_repository.get_by_user_id(
            user.id
        )

        if customer is None:
            raise ValueError(
                "Customer profile not found."
            )

        service = self.service_repository.get_by_id(
            request.service_id
        )

        if service is None:
            raise ValueError(
                "Service not found."
            )

        booking = Booking(
            customer_id=customer.id,
            provider_id=service.provider_id,
            service_id=service.id,
            booking_date=request.booking_date,
            customer_notes=request.customer_notes,
            status=BookingStatus.PENDING,
        )

        return self.booking_repository.create(
            booking
        )

    # =====================================================
    # GET BOOKING
    # =====================================================

    def get_booking(
        self,
        booking_id: int,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        return booking

    # =====================================================
    # LIST BOOKINGS
    # =====================================================

    def list_bookings(self) -> list[Booking]:
        """
        Return all bookings.
        """

        return self.booking_repository.list_bookings()

    # =====================================================
    # UPDATE BOOKING
    # =====================================================

    def update_booking(
        self,
        booking_id: int,
        request: BookingUpdate,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        if request.booking_date is not None:
            booking.booking_date = request.booking_date

        if request.customer_notes is not None:
            booking.customer_notes = request.customer_notes

        return self.booking_repository.update(
            booking
        )

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    def update_status(
        self,
        booking_id: int,
        status: BookingStatus,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        booking.status = status

        return self.booking_repository.update(
            booking
        )

    # =====================================================
    # DELETE BOOKING
    # =====================================================

    def delete_booking(
        self,
        booking_id: int,
    ) -> None:

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        self.booking_repository.delete(
            booking
        )
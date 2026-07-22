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
            service_id=service.id,
            booking_date=request.booking_date,
            customer_note=request.customer_note,
            status=BookingStatus.PENDING,
        )

        return self.booking_repository.create(
            booking
        )

    # =====================================================
    # ACCESS CONTROL HELPER
    # =====================================================

    def _assert_can_access(
        self,
        booking: Booking,
        user: User,
    ) -> None:
        """
        Ensure the requesting user owns this booking
        (as the customer or the provider), or is an admin.
        """

        if user.role.value == "ADMIN":
            return

        customer = self.customer_repository.get_by_user_id(
            user.id
        )

        if customer is not None and booking.customer_id == customer.id:
            return

        provider = self.provider_repository.get_by_user_id(
            user.id
        )

        if provider is not None and booking.provider_id == provider.id:
            return

        raise ValueError(
            "You do not have permission to access this booking."
        )

    # =====================================================
    # GET BOOKING
    # =====================================================

    def get_booking(
        self,
        booking_id: int,
        user: User,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        self._assert_can_access(booking, user)

        return booking

    # =====================================================
    # LIST BOOKINGS
    # =====================================================

    def list_bookings(self, user: User) -> list[Booking]:
        """
        Return bookings visible to the requesting user:
        - Admins see every booking.
        - Customers see their own bookings.
        - Providers see bookings made against their services.
        """

        if user.role.value == "ADMIN":
            return self.booking_repository.list_bookings()

        customer = self.customer_repository.get_by_user_id(
            user.id
        )

        if customer is not None:
            return self.booking_repository.get_customer_bookings(
                customer.id
            )

        provider = self.provider_repository.get_by_user_id(
            user.id
        )

        if provider is not None:
            return self.booking_repository.get_provider_bookings(
                provider.id
            )

        return []

    # =====================================================
    # UPDATE BOOKING
    # =====================================================

    def update_booking(
        self,
        booking_id: int,
        request: BookingUpdate,
        user: User,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        self._assert_can_access(booking, user)

        if request.booking_date is not None:
            booking.booking_date = request.booking_date

        if request.customer_note is not None:
            booking.customer_note = request.customer_note

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
        user: User,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        self._assert_can_access(booking, user)

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
        user: User,
    ) -> None:

        booking = self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        self._assert_can_access(booking, user)

        self.booking_repository.delete(
            booking
        )
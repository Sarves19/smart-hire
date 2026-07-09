"""
Payment Service

Contains business logic for payment management.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.payment import Payment, PaymentStatus
from app.repositories.booking_repository import BookingRepository
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
)


class PaymentService:
    """
    Handles payment business logic.
    """

    def __init__(self, db: Session):
        self.payment_repository = PaymentRepository(db)
        self.booking_repository = BookingRepository(db)

    # =====================================================
    # CREATE PAYMENT
    # =====================================================

    def create_payment(
        self,
        request: PaymentCreate,
    ) -> Payment:
        """
        Create a payment.
        """

        booking = self.booking_repository.get_by_id(
            request.booking_id
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        existing_payment = self.payment_repository.get_by_booking(
            request.booking_id
        )

        if existing_payment:
            raise ValueError(
                "Payment already exists for this booking."
            )

        payment = Payment(
            booking_id=request.booking_id,
            amount=request.amount,
            payment_method=request.payment_method,
            status=PaymentStatus.PENDING,
            transaction_id=str(uuid4()),
        )

        return self.payment_repository.create(
            payment
        )

    # =====================================================
    # GET PAYMENT
    # =====================================================

    def get_payment(
        self,
        payment_id: int,
    ) -> Payment:

        payment = self.payment_repository.get_by_id(
            payment_id
        )

        if payment is None:
            raise ValueError(
                "Payment not found."
            )

        return payment

    # =====================================================
    # LIST PAYMENTS
    # =====================================================

    def list_payments(self) -> list[Payment]:

        return self.payment_repository.list_payments()

    # =====================================================
    # UPDATE PAYMENT
    # =====================================================

    def update_payment(
        self,
        payment_id: int,
        request: PaymentUpdate,
    ) -> Payment:

        payment = self.payment_repository.get_by_id(
            payment_id
        )

        if payment is None:
            raise ValueError(
                "Payment not found."
            )

        if request.payment_method is not None:
            payment.payment_method = request.payment_method

        return self.payment_repository.update(
            payment
        )

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    def update_status(
        self,
        payment_id: int,
        status: PaymentStatus,
    ) -> Payment:

        payment = self.payment_repository.get_by_id(
            payment_id
        )

        if payment is None:
            raise ValueError(
                "Payment not found."
            )

        payment.status = status

        if status == PaymentStatus.SUCCESS:
            payment.paid_at = datetime.utcnow()

        return self.payment_repository.update(
            payment
        )

    # =====================================================
    # DELETE PAYMENT
    # =====================================================

    def delete_payment(
        self,
        payment_id: int,
    ) -> None:

        payment = self.payment_repository.get_by_id(
            payment_id
        )

        if payment is None:
            raise ValueError(
                "Payment not found."
            )

        self.payment_repository.delete(
            payment
        )
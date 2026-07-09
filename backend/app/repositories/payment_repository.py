"""
Payment Repository

Handles all database operations related to payments.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:
    """
    Repository responsible for payment operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        payment: Payment,
    ) -> Payment:
        """
        Create a payment.
        """

        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)

        return payment

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(
        self,
        payment_id: int,
    ) -> Optional[Payment]:
        """
        Get payment by ID.
        """

        stmt = select(Payment).where(
            Payment.id == payment_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_booking(
        self,
        booking_id: int,
    ) -> Optional[Payment]:
        """
        Get payment by booking ID.
        """

        stmt = select(Payment).where(
            Payment.booking_id == booking_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def list_payments(self) -> list[Payment]:
        """
        Return all payments.
        """

        stmt = select(Payment)

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        payment: Payment,
    ) -> Payment:
        """
        Update payment.
        """

        self.db.commit()
        self.db.refresh(payment)

        return payment

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        payment: Payment,
    ) -> None:
        """
        Delete payment.
        """

        self.db.delete(payment)
        self.db.commit()

        
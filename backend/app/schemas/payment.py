"""
Payment Schemas

Pydantic models for payment management.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# CREATE PAYMENT
# =====================================================

class PaymentCreate(BaseModel):
    """
    Request schema for creating a payment.
    """

    booking_id: int

    amount: Decimal = Field(
        ...,
        gt=0,
    )

    payment_method: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )


# =====================================================
# UPDATE PAYMENT
# =====================================================

class PaymentUpdate(BaseModel):
    """
    Request schema for updating a payment.
    """

    payment_method: Optional[str] = None


# =====================================================
# PAYMENT STATUS
# =====================================================

class PaymentStatusUpdate(BaseModel):
    """
    Update payment status.
    """

    status: str


# =====================================================
# PAYMENT RESPONSE
# =====================================================

class PaymentResponse(BaseModel):
    """
    Payment response.
    """

    id: int

    booking_id: int

    amount: Decimal

    payment_method: str

    status: str

    transaction_id: Optional[str]

    paid_at: Optional[datetime]

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
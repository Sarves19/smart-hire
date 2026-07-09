"""
Booking Schemas

Pydantic models for booking management.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# CREATE BOOKING
# =====================================================

class BookingCreate(BaseModel):
    """
    Request schema for creating a booking.
    """

    service_id: int

    booking_date: datetime

    customer_notes: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


# =====================================================
# UPDATE BOOKING
# =====================================================

class BookingUpdate(BaseModel):
    """
    Request schema for updating a booking.
    """

    booking_date: Optional[datetime] = None

    customer_notes: Optional[str] = None


# =====================================================
# STATUS UPDATE
# =====================================================

class BookingStatusUpdate(BaseModel):
    """
    Update booking status.
    """

    status: str


# =====================================================
# BOOKING RESPONSE
# =====================================================

class BookingResponse(BaseModel):
    """
    Booking response.
    """

    id: int

    customer_id: int

    provider_id: int

    service_id: int

    booking_date: datetime

    status: str

    customer_notes: Optional[str]

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
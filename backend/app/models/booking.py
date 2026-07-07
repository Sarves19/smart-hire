"""
Booking Model

Stores customer bookings for services.
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class BookingStatus(str, Enum):
    """
    Booking Status
    """

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Booking(BaseModel):
    """
    Booking Model
    """

    __tablename__ = "bookings"

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    booking_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    status: Mapped[BookingStatus] = mapped_column(
        SqlEnum(BookingStatus),
        default=BookingStatus.PENDING,
        nullable=False,
    )

    customer_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    provider_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cancellation_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

customer: Mapped["CustomerProfile"] = relationship(
    back_populates="bookings",
)

service: Mapped["Service"] = relationship(
    back_populates="bookings",
)

payment: Mapped["Payment"] = relationship(
    back_populates="booking",
    uselist=False,
    cascade="all, delete-orphan",
)

review: Mapped["Review"] = relationship(
    back_populates="booking",
    uselist=False,
    cascade="all, delete-orphan",
)

def __repr__(self):
        return (
            f"<Booking(id={self.id}, status='{self.status.value}')>"
        )
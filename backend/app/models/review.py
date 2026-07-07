"""
Review Model

Stores customer reviews for completed services.
"""

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Review(BaseModel):
    """
    Review Model
    """

    __tablename__ = "reviews"

    booking_id: Mapped[int] = mapped_column(
        ForeignKey("bookings.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

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

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

booking: Mapped["Booking"] = relationship(
    back_populates="review",
)

customer: Mapped["CustomerProfile"] = relationship(
    back_populates="reviews",
)

service: Mapped["Service"] = relationship(
    back_populates="reviews",
)

__table_args__ = (
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="check_rating_range",
        ),
    )

def __repr__(self):
        return (
            f"<Review(id={self.id}, rating={self.rating})>"
        )
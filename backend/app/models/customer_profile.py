"""
Customer Profile Model

Stores customer-specific information.
"""

from app.models.user import User
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class CustomerProfile(BaseModel):
    """
    Customer Profile
    """

    __tablename__ = "customer_profiles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    profile_image: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    district: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

customer: Mapped["User"] = relationship(
    back_populates="customer_profile",
)

bookings: Mapped[list["Booking"]] = relationship(
    back_populates="customer",
    cascade="all, delete-orphan",
)

reviews: Mapped[list["Review"]] = relationship(
    back_populates="customer",
    cascade="all, delete-orphan",
)

recommendations: Mapped[list["Recommendation"]] = relationship(
    back_populates="customer",
    cascade="all, delete-orphan",
)
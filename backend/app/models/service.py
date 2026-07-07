"""
Service Model

Stores services offered by service providers.
"""

from __future__ import annotations

from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Boolean,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ServiceStatus(str, Enum):
    """
    Service Status
    """

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"


class Service(BaseModel):
    """
    Service Model
    """

    __tablename__ = "services"

    provider_id: Mapped[int] = mapped_column(
        ForeignKey("provider_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    service_location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    image_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    status: Mapped[ServiceStatus] = mapped_column(
        SqlEnum(ServiceStatus),
        default=ServiceStatus.PENDING,
        nullable=False,
    )

    # ==========================================
    # Relationships
    # ==========================================

    provider: Mapped["ProviderProfile"] = relationship(
        "ProviderProfile",
        back_populates="services",
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="services",
    )

    bookings: Mapped[list["Booking"]] = relationship(
        "Booking",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    recommendations: Mapped[list["Recommendation"]] = relationship(
        "Recommendation",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Service(title='{self.title}', price={self.price})>"
        )
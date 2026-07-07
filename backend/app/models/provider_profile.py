"""
Provider Profile Model

Stores service provider-specific information.
"""

from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ProviderProfile(BaseModel):
    """
    Service Provider Profile
    """

    __tablename__ = "provider_profiles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    business_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    business_registration_number: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    years_of_experience: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    business_address: Mapped[str | None] = mapped_column(
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

    service_radius_km: Mapped[float] = mapped_column(
        Float,
        default=10.0,
        nullable=False,
    )

    business_logo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ==========================================
    # Relationships
    # ==========================================

    provider: Mapped["User"] = relationship(
        "User",
        back_populates="provider_profile",
    )

    services: Mapped[list["Service"]] = relationship(
        "Service",
        back_populates="provider",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<ProviderProfile(id={self.id}, business='{self.business_name}')>"
        )
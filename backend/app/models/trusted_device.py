"""
Trusted Device Model

Stores trusted devices that can skip OTP verification on login.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.user import User


class TrustedDevice(BaseModel):
    """
    Trusted Device Model - allows users to skip OTP on known devices for 30 days.
    """

    __tablename__ = "trusted_devices"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    device_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    device_fingerprint: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=True,
        index=True,
    )

    browser: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    operating_system: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        default=True,
        nullable=False,
    )

    last_used_at: Mapped[datetime] = mapped_column(
        nullable=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc) + timedelta(days=30),
        nullable=False,
    )

    # Relationships
    user: Mapped[User] = relationship(
        "User",
        back_populates="trusted_devices",
    )

    def is_expired(self) -> bool:
        """Check if device trust has expired."""
        return datetime.now(timezone.utc) > self.expires_at

    def is_valid(self) -> bool:
        """Check if device is valid and not expired."""
        return self.is_active and not self.is_expired()

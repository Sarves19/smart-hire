"""
Login History Model

Stores login records for audit trail and suspicious login detection.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Boolean, Enum as SqlEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.user import User


class LoginStatus(str, Enum):
    """Login outcome status"""
    SUCCESS = "SUCCESS"
    FAILED_INVALID_CREDENTIALS = "FAILED_INVALID_CREDENTIALS"
    FAILED_OTP_INVALID = "FAILED_OTP_INVALID"
    FAILED_ACCOUNT_INACTIVE = "FAILED_ACCOUNT_INACTIVE"
    FAILED_EMAIL_UNVERIFIED = "FAILED_EMAIL_UNVERIFIED"
    FAILED_ACCOUNT_LOCKED = "FAILED_ACCOUNT_LOCKED"


class LoginHistory(BaseModel):
    """
    Login History Model - tracks all login attempts for security audit trail.
    """

    __tablename__ = "login_history"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=True,
    )

    browser: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    operating_system: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    device: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    device_fingerprint: Mapped[str] = mapped_column(
        String(512),
        nullable=True,
    )

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[LoginStatus] = mapped_column(
        SqlEnum(LoginStatus),
        default=LoginStatus.SUCCESS,
        nullable=False,
    )

    is_trusted_device: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
        nullable=False,
    )

    failure_reason: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    notification_sent: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
        nullable=False,
    )

    # Relationships
    user: Mapped[User] = relationship(
        "User",
        back_populates="login_history",
    )

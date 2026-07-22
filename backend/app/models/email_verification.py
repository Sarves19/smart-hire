"""
Email Verification Model

Stores one-time-password (OTP) codes used for email
verification and password reset flows.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class OtpPurpose(str, Enum):
    """
    What a given OTP code is valid for. Kept separate so a
    verification-email OTP can never be replayed to reset a
    password, and vice versa.
    """

    EMAIL_VERIFICATION = "EMAIL_VERIFICATION"
    PASSWORD_RESET = "PASSWORD_RESET"


class EmailVerification(BaseModel):
    """
    Email Verification / OTP table.
    """

    __tablename__ = "email_verifications"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # The OTP is never stored in plain text - only its Argon2
    # hash, the same way passwords are hashed.
    otp_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    purpose: Mapped[OtpPurpose] = mapped_column(
        SqlEnum(OtpPurpose),
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    is_used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # ==========================================
    # Relationships
    # ==========================================

    user: Mapped["User"] = relationship(
        "User",
        back_populates="email_verifications",
    )

    def __repr__(self) -> str:
        return (
            f"<EmailVerification(id={self.id}, "
            f"user_id={self.user_id}, "
            f"purpose='{self.purpose.value}')>"
        )

"""
Notification Model

Stores notifications sent to users.
"""

from __future__ import annotations

from enum import Enum

from sqlalchemy import Boolean, Enum as SqlEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class NotificationType(str, Enum):
    """
    Notification Types
    """

    BOOKING = "BOOKING"
    PAYMENT = "PAYMENT"
    REVIEW = "REVIEW"
    SYSTEM = "SYSTEM"


class Notification(BaseModel):
    """
    Notification Model
    """

    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    notification_type: Mapped[NotificationType] = mapped_column(
        SqlEnum(NotificationType),
        nullable=False,
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ==========================================
    # Relationships
    # ==========================================

    user: Mapped["User"] = relationship(
        "User",
        back_populates="notifications",
    )

    def __repr__(self) -> str:
        return (
            f"<Notification(id={self.id}, title='{self.title}')>"
        )
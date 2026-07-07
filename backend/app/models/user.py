"""
User Model

Represents all users in the Smart Hire system.
"""

from __future__ import annotations

from enum import Enum

from sqlalchemy import Boolean, Enum as SqlEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class UserRole(str, Enum):
    """
    Available user roles.
    """

    CUSTOMER = "CUSTOMER"
    PROVIDER = "PROVIDER"
    ADMIN = "ADMIN"


class User(BaseModel):
    """
    User table.
    """

    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ==========================================
    # Relationships
    # ==========================================

    customer_profile: Mapped["CustomerProfile"] = relationship(
        "CustomerProfile",
        back_populates="customer",
        uselist=False,
        cascade="all, delete-orphan",
    )

    provider_profile: Mapped["ProviderProfile"] = relationship(
        "ProviderProfile",
        back_populates="provider",
        uselist=False,
        cascade="all, delete-orphan",
    )

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, "
            f"email='{self.email}', "
            f"role='{self.role.value}')>"
        )
    
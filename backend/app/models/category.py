"""
Category Model

Stores service categories.
"""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Category(BaseModel):
    """
    Service Category Model
    """

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    icon: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    # One Category -> Many Services
services: Mapped[list["Service"]] = relationship(
    back_populates="category",
    cascade="all, delete-orphan",
)

def __repr__(self) -> str:
        return f"<Category(name='{self.name}')>"
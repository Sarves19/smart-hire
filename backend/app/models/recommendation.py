"""
Recommendation Model

Stores AI-generated service recommendations for customers.
"""

from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Recommendation(BaseModel):
    """
    AI Recommendation Model
    """

    __tablename__ = "recommendations"

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

    recommendation_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

customer: Mapped["CustomerProfile"] = relationship(
    back_populates="recommendations",
)

service: Mapped["Service"] = relationship(
    back_populates="recommendations",
)

def __repr__(self):
        return (
            f"<Recommendation(customer_id={self.customer_id}, "
            f"service_id={self.service_id}, "
            f"score={self.recommendation_score})>"
        )
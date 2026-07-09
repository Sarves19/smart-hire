"""
Review Schemas

Pydantic models for review management.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# CREATE REVIEW
# =====================================================

class ReviewCreate(BaseModel):
    """
    Request schema for creating a review.
    """

    booking_id: int

    rating: int = Field(
        ...,
        ge=1,
        le=5,
    )

    comment: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


# =====================================================
# UPDATE REVIEW
# =====================================================

class ReviewUpdate(BaseModel):
    """
    Request schema for updating a review.
    """

    rating: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,
    )

    comment: Optional[str] = None


# =====================================================
# REVIEW RESPONSE
# =====================================================

class ReviewResponse(BaseModel):
    """
    Review response.
    """

    id: int

    booking_id: int

    customer_id: int

    provider_id: int

    rating: int

    comment: Optional[str]

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
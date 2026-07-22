"""
Service Schemas

Pydantic models for service management.
"""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# Create Service
# =====================================================

class ServiceCreate(BaseModel):
    """
    Request schema for creating a service.
    """

    category_id: int

    title: str = Field(
        ...,
        min_length=3,
        max_length=150,
    )

    description: str = Field(
        ...,
        min_length=10,
    )

    price: Decimal = Field(
        ...,
        gt=0,
    )

    duration_minutes: int = Field(
        ...,
        gt=0,
    )

    service_location: Optional[str] = None

    image_url: Optional[str] = None


# =====================================================
# Update Service
# =====================================================

class ServiceUpdate(BaseModel):
    """
    Request schema for updating a service.
    """

    category_id: Optional[int] = None

    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=150,
    )

    description: Optional[str] = None

    price: Optional[Decimal] = Field(
        default=None,
        gt=0,
    )

    duration_minutes: Optional[int] = Field(
        default=None,
        gt=0,
    )

    service_location: Optional[str] = None

    image_url: Optional[str] = None

    is_available: Optional[bool] = None


# =====================================================
# Service Response
# =====================================================

class ServiceResponse(BaseModel):
    """
    Service response schema.
    """

    id: int

    provider_id: int

    category_id: int

    title: str

    description: str

    price: Decimal

    duration_minutes: int

    service_location: Optional[str]

    image_url: Optional[str]

    is_available: bool

    status: str

    provider_name: str
    category_name: str
    average_rating: float
    review_count: int

    model_config = ConfigDict(
        from_attributes=True,
    )
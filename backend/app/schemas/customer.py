"""
Customer Profile Schemas
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CustomerProfileCreate(BaseModel):
    """
    Create customer profile.
    """

    profile_image: Optional[str] = None

    address: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    city: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    district: Optional[str] = Field(
        default=None,
        max_length=100,
    )


class CustomerProfileUpdate(BaseModel):
    """
    Update customer profile.
    """

    profile_image: Optional[str] = None

    address: Optional[str] = Field(
        default=None,
        max_length=255,
    )

    city: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    district: Optional[str] = Field(
        default=None,
        max_length=100,
    )


class CustomerProfileResponse(BaseModel):
    """
    Customer profile response.
    """

    id: int
    user_id: int

    profile_image: Optional[str]
    address: Optional[str]
    city: Optional[str]
    district: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
    )
"""
Customer Profile Schemas
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def validate_uploaded_image_url(value: Optional[str]) -> Optional[str]:
    if value is not None and not value.startswith("/uploads/profile-images/"):
        raise ValueError("Profile images must be uploaded through the profile image endpoint.")
    return value


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

    _validate_image = field_validator("profile_image")(validate_uploaded_image_url)


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

    _validate_image = field_validator("profile_image")(validate_uploaded_image_url)


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

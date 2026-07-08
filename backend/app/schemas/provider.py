"""
Provider Profile Schemas

Pydantic models for provider profile requests and responses.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# Create Provider Profile
# =====================================================

class ProviderProfileCreate(BaseModel):
    """
    Request schema for creating a provider profile.
    """

    business_name: str = Field(..., max_length=150)

    business_registration_number: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    description: Optional[str] = None

    years_of_experience: int = Field(
        default=0,
        ge=0,
    )

    business_address: Optional[str] = Field(
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

    service_radius_km: float = Field(
        default=10.0,
        ge=0,
    )

    business_logo: Optional[str] = None


# =====================================================
# Update Provider Profile
# =====================================================

class ProviderProfileUpdate(BaseModel):
    """
    Request schema for updating a provider profile.
    """

    business_name: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    business_registration_number: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    description: Optional[str] = None

    years_of_experience: Optional[int] = Field(
        default=None,
        ge=0,
    )

    business_address: Optional[str] = Field(
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

    service_radius_km: Optional[float] = Field(
        default=None,
        ge=0,
    )

    business_logo: Optional[str] = None


# =====================================================
# Provider Profile Response
# =====================================================

class ProviderProfileResponse(BaseModel):
    """
    Response schema for provider profile.
    """

    id: int
    user_id: int

    business_name: str
    business_registration_number: Optional[str]
    description: Optional[str]

    years_of_experience: int

    business_address: Optional[str]
    city: Optional[str]
    district: Optional[str]

    service_radius_km: float

    business_logo: Optional[str]

    is_verified: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
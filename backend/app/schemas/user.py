"""
User Schemas

Pydantic models used for user-related requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# =====================================================
# Customer Profile
# =====================================================

class CustomerProfileResponse(BaseModel):
    """
    Customer profile response.
    """

    profile_image: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Provider Profile
# =====================================================

class ProviderProfileResponse(BaseModel):
    """
    Provider profile response.
    """

    business_name: str
    business_registration_number: Optional[str] = None
    description: Optional[str] = None
    years_of_experience: int
    business_address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    service_radius_km: float
    business_logo: Optional[str] = None
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# User Response
# =====================================================

class UserResponse(BaseModel):
    """
    Basic user response.
    """

    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Complete User Profile
# =====================================================

class UserProfileResponse(UserResponse):
    """
    Complete user profile response.
    """

    customer_profile: Optional[CustomerProfileResponse] = None
    provider_profile: Optional[ProviderProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Update User
# =====================================================

class UserUpdateRequest(BaseModel):
    """
    Update user profile request.
    """

    first_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    last_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    phone_number: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=20,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Sarves",
                "last_name": "Suresh",
                "phone_number": "0771234567"
            }
        }
    )
"""
User Schemas

Pydantic models used for user-related requests and responses.
"""

from datetime import datetime
import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


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

    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = " ".join(value.split())
        if not value.replace(" ", "").isalpha():
            raise ValueError("Names may contain letters and spaces only.")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not re.fullmatch(r"(?:\+94|0)7\d{8}", value):
            raise ValueError("Enter a valid Sri Lankan mobile number.")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Sarves",
                "last_name": "Suresh",
                "phone_number": "0771234567"
            }
        }
    )


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=1, max_length=128)
    new_password: str = Field(..., min_length=12, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not all((
            re.search(r"[a-z]", value),
            re.search(r"[A-Z]", value),
            re.search(r"\d", value),
            re.search(r"[^A-Za-z0-9]", value),
        )):
            raise ValueError("Password must include uppercase, lowercase, number, and symbol.")
        return value

    @model_validator(mode="after")
    def passwords_must_differ(self):
        if self.current_password == self.new_password:
            raise ValueError("New password must be different from the current password.")
        return self


class UserStatusUpdateRequest(BaseModel):
    is_active: bool


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int

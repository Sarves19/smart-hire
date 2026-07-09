from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username:str
    email:str
    password: str

class CustomerCreate(UserBase):
    role: str = "customer"

class ProviderCreate(UserBase):

    role: str = "provider"
    service_type: str | None = None
    experience_years: int = 0
    hourly_rate: float =0.0
    location: str

class ProviderResponse(BaseModel):
    id: int # providers.id
    user_id: int # users.id
    service_type: str
    experience_years: int
    hourly_rate: float
    location: str
    is_available: bool
    rating: float

    class Config:
        from_attributes = True

class ProviderUpdate(BaseModel):
    bio: Optional[str] = None
    experience_years: int
    hourly_rate: float
    service_type: Optional[str] = None
    is_available: bool
    location: Optional[str] = None


class UserResponse(UserBase):
    id: int
    role: str
    provider_profile: ProviderResponse = None

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    provider_profile_id: int
    job_title: str
    description: Optional[str] = None
    booking_date: datetime

class BookingUpdateStatus(BaseModel):
    status: str


class BookingResponse(BaseModel):
    id: int
    customer_id: int
    provider_id: int
    job_title: str
    description: Optional[str]
    status: str = "pending"
    booking_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type:str
    role:str


class ReviewCreate(BaseModel):
    rating: float = Field(..., gte=1.0, lte=5.0, description="rating must be between 1.0 and 5.0" )
    comment: Optional[str] = Field(None, max_length=500, description="Optional text review")
    provider_id: int
    review_date: datetime

class ReviewResponse(BaseModel):
    id: int
    rating: float
    comment: Optional[str]
    review_date: datetime
    customer_id: int
    provider_id: int

    class Config:
        from_attributes = True


class CustomerDashboardMetrics(BaseModel):
    total_bookings: int
    pending_bookings: int
    accepted_bookings:int
    completed_bookings:int
    rejected_bookings:int

class ProviderDashboardMetrics(BaseModel):
    total_bookings: int
    pending_bookings: int
    accepted_bookings: int
    completed_bookings: int
    rejected_bookings: int
    average_rating: float
    total_reviews: int


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    category_id: int
    name: str
    description: Optional[str]
    status: bool

    class Config:
        from_attributes = True


class ServiceCreate(BaseModel):
    category_id: int
    title: str
    description: Optional[str] = None
    price: Decimal
    duration: str

class ServiceResponse(BaseModel):
    service_id: int
    provider_id: int
    category_id: int
    title: str
    description: Optional[str]
    price: Decimal
    duration: str
    status: str

    class Config:
        from_attributes = True
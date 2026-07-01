from datetime import datetime

from pydantic import BaseModel, EmailStr


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

class ProviderProfileResponse(BaseModel):
    service_type: str
    experience_years: int
    hourly_rate: float
    location: str
    is_available: bool
    rating: float

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    role: str
    provider_profile: ProviderProfileResponse | None = None

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    job_title: str
    description: str | None = None

class BookingCreate(BookingBase):

    user_id: int

class BookingResponse(BookingBase):
    id: int
    user_id: int
    status: str
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
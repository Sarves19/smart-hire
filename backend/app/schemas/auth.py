"""
Authentication Schemas

Pydantic models used for authentication requests and responses.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    """
    User registration request.
    """

    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)
    role: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone_number": "0771234567",
                "password": "StrongPassword123!",
                "role": "CUSTOMER",
            }
        }
    )


class LoginRequest(BaseModel):
    """
    User login request.
    """

    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john@example.com",
                "password": "StrongPassword123!",
            }
        }
    )


class TokenResponse(BaseModel):
    """
    JWT token response.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """
    Refresh token request.
    """

    refresh_token: str



class RefreshTokenResponse(BaseModel):
    """
    Response schema for a refreshed access token.
    """

    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    """
    Generic message response.
    """

    message: str
"""
Authentication Schemas

Pydantic models used for authentication requests and responses.
"""

import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from app.models.user import UserRole


class EmailRequest(BaseModel):
    """Normalize email identities before every authentication lookup."""

    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class RegisterRequest(EmailRequest):
    """
    User registration request.
    """

    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=8, max_length=128)
    role: UserRole

    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = " ".join(value.split())
        if not value.replace(" ", "").isalpha():
            raise ValueError("Names may contain letters and spaces only.")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        value = value.strip()
        if not re.fullmatch(r"(?:\+94|0)7\d{8}", value):
            raise ValueError("Enter a valid Sri Lankan mobile number.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not all((
            re.search(r"[a-z]", value),
            re.search(r"[A-Z]", value),
            re.search(r"\d", value),
            re.search(r"[^A-Za-z0-9]", value),
        )):
            raise ValueError(
                "Password must include uppercase, lowercase, number, and symbol."
            )
        return value

    @model_validator(mode="after")
    def reject_password_based_on_identity(self):
        lowered = self.password.lower()
        if any(part.lower() in lowered for part in (self.first_name, self.last_name, self.email.split("@")[0])):
            raise ValueError("Password must not contain your name or email address.")
        return self

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


class LoginRequest(EmailRequest):
    """
    User login request.
    """

    password: str = Field(..., min_length=1, max_length=128)

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
    refresh_token: str | None = Field(default=None, min_length=1, max_length=4096)
    token_type: str = "bearer"
    user: dict | None = Field(default=None)


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


class VerifyOtpRequest(EmailRequest):
    """
    Verify the OTP sent after registration to activate the
    account.
    """

    otp_code: str = Field(..., pattern=r"^\d{6}$")


class ResendOtpRequest(EmailRequest):
    """
    Request a new email-verification OTP (e.g. the first one
    expired or was never received).
    """



class ForgotPasswordRequest(EmailRequest):
    """
    Request a password-reset OTP.
    """



class ResetPasswordRequest(EmailRequest):
    """
    Reset the password using a verified OTP.
    """

    otp_code: str = Field(..., pattern=r"^\d{6}$")
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        return RegisterRequest.validate_password_strength(value)


class LoginVerifyRequest(EmailRequest):
    """
    Verify login OTP and receive JWT tokens.
    """

    otp_code: str = Field(..., pattern=r"^\d{6}$")
    device_fingerprint: str | None = Field(default=None, max_length=512)
    device_name: str | None = Field(default=None, max_length=255)
    browser: str | None = Field(default=None, max_length=100)
    operating_system: str | None = Field(default=None, max_length=100)
    ip_address: str | None = Field(default=None, max_length=45)
    remember_device: bool = Field(default=False)


class LogoutRequest(BaseModel):
    """
    Logout request.
    """

    device_fingerprint: str | None = Field(default=None, max_length=512)


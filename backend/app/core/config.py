"""
Smart Hire Configuration Module
"""

from functools import lru_cache

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings
    """

    # =====================================================
    # Application
    # =====================================================

    APP_NAME: str = "Smart Hire"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # =====================================================
    # Server
    # =====================================================

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # =====================================================
    # Database
    # =====================================================

    DATABASE_URL: str

    # =====================================================
    # JWT
    # =====================================================

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    CORS_ORIGINS: list[str] = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ]

    # =====================================================
    # AI / OpenRouter
    # =====================================================

    OPENROUTER_API_KEY: str = ""

    OPENROUTER_MODEL: str = "openai/gpt-4.1-mini"

    LANGCHAIN_API_KEY: str = ""

    # =====================================================
    # Azure
    # =====================================================

    AZURE_STORAGE_CONNECTION_STRING: str = ""
    AZURE_CONTAINER_NAME: str = ""

    # =====================================================
    # Email / SMTP
    # =====================================================

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "Smart Hire"

    # Port 465 = implicit TLS (SMTP_SSL from the first byte).
    # Port 587 = plaintext connect, then STARTTLS upgrade.
    # These are NOT interchangeable - using SMTP() + starttls()
    # against port 465 is what produces
    # "SMTPServerDisconnected: please run connect() first",
    # because Gmail closes the raw (non-TLS) socket immediately.
    SMTP_USE_SSL: bool = True

    # =====================================================
    # OTP
    # =====================================================

    OTP_LENGTH: int = 6
    OTP_EXPIRY_MINUTES: int = 10
    OTP_MAX_ATTEMPTS: int = 5

    # =====================================================
    # Logging
    # =====================================================

    LOG_LEVEL: str = "INFO"

    @field_validator("ALGORITHM")
    @classmethod
    def require_supported_jwt_algorithm(cls, value: str) -> str:
        if value != "HS256":
            raise ValueError("ALGORITHM must be HS256.")
        return value

    @model_validator(mode="after")
    def validate_security_settings(self):
        if len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long.")
        if self.ACCESS_TOKEN_EXPIRE_MINUTES <= 0 or self.ACCESS_TOKEN_EXPIRE_MINUTES > 60:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be between 1 and 60.")
        if self.REFRESH_TOKEN_EXPIRE_DAYS <= 0 or self.REFRESH_TOKEN_EXPIRE_DAYS > 30:
            raise ValueError("REFRESH_TOKEN_EXPIRE_DAYS must be between 1 and 30.")
        
        # Validate SMTP configuration for email features
        if self.SMTP_USERNAME or self.SMTP_PASSWORD:
            # If one is set, both must be set
            missing_smtp = []
            if not self.SMTP_HOST:
                missing_smtp.append("SMTP_HOST")
            if not self.SMTP_PORT:
                missing_smtp.append("SMTP_PORT")
            if not self.SMTP_USERNAME:
                missing_smtp.append("SMTP_USERNAME")
            if not self.SMTP_PASSWORD:
                missing_smtp.append("SMTP_PASSWORD")
            if not self.SMTP_FROM_EMAIL:
                missing_smtp.append("SMTP_FROM_EMAIL")
            
            if missing_smtp:
                raise ValueError(
                    f"Email (SMTP) configuration incomplete. Missing: {', '.join(missing_smtp)}. "
                    "Set these in backend/.env to enable email features (registration OTP, login OTP, "
                    "login notifications, password reset). "
                    "For Gmail: use SMTP_PASSWORD as the 16-character App Password, not your regular password."
                )
            
            # Validate port is numeric and in valid range
            if self.SMTP_PORT not in [25, 465, 587, 2525]:
                raise ValueError(
                    f"SMTP_PORT must be 25, 465, 587, or 2525, got {self.SMTP_PORT}. "
                    "Port 465=SSL (use SMTP_USE_SSL=True), Port 587=STARTTLS (use SMTP_USE_SSL=False)."
                )
        
        # Validate OTP settings
        if self.OTP_LENGTH <= 0:
            raise ValueError("OTP_LENGTH must be greater than 0.")
        if self.OTP_EXPIRY_MINUTES <= 0:
            raise ValueError("OTP_EXPIRY_MINUTES must be greater than 0.")
        if self.OTP_MAX_ATTEMPTS <= 0:
            raise ValueError("OTP_MAX_ATTEMPTS must be greater than 0.")
        
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

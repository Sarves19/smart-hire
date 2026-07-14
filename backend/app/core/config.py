"""
Smart Hire Configuration Module
"""

from functools import lru_cache

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

    # =====================================================
    # AI / OpenRouter
    # =====================================================

    OPENROUTER_API_KEY: str = "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"

    OPENROUTER_MODEL: str = "openai/gpt-4.1-mini"

    LANGCHAIN_API_KEY: str = ""

    # =====================================================
    # Azure
    # =====================================================

    AZURE_STORAGE_CONNECTION_STRING: str = ""
    AZURE_CONTAINER_NAME: str = ""

    # =====================================================
    # Logging
    # =====================================================

    LOG_LEVEL: str = "INFO"

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
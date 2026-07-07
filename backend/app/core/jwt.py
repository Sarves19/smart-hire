"""
JWT Utility Module

Handles JWT access token creation, refresh token creation,
token decoding, and token verification.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.core.config import settings


class JWTManager:
    """
    Handles JWT token generation and verification.
    """

    def __init__(self) -> None:
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire = settings.REFRESH_TOKEN_EXPIRE_DAYS

    # =====================================================
    # Access Token
    # =====================================================

    def create_access_token(
        self,
        subject: str,
        additional_claims: dict[str, Any] | None = None,
    ) -> str:
        """
        Create a JWT access token.
        """

        payload = {
            "sub": subject,
            "type": "access",
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self.access_token_expire),
            "iat": datetime.now(timezone.utc),
        }

        if additional_claims:
            payload.update(additional_claims)

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    # =====================================================
    # Refresh Token
    # =====================================================

    def create_refresh_token(
        self,
        subject: str,
    ) -> str:
        """
        Create a JWT refresh token.
        """

        payload = {
            "sub": subject,
            "type": "refresh",
            "exp": datetime.now(timezone.utc)
            + timedelta(days=self.refresh_token_expire),
            "iat": datetime.now(timezone.utc),
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    # =====================================================
    # Decode Token
    # =====================================================

    def decode_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Decode a JWT token.
        """

        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )

    # =====================================================
    # Verify Token
    # =====================================================

    def verify_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Verify and return the decoded JWT payload.
        """

        try:
            return self.decode_token(token)

        except JWTError as exc:
            raise JWTError("Invalid or expired token.") from exc


jwt_manager = JWTManager()
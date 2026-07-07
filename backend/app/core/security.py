"""
Security Module

Handles password hashing and verification using Argon2.

This module is responsible for:
- Password hashing
- Password verification
- OAuth2 Bearer Token configuration
"""

from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash


class PasswordManager:
    """
    Provides password hashing and verification utilities.
    """

    def __init__(self) -> None:
        """
        Initialize the Argon2 password hasher.
        """
        self.password_hasher = PasswordHash.recommended()

    def hash_password(
        self,
        password: str,
    ) -> str:
        """
        Hash a plain text password.
        """

        return self.password_hasher.hash(password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a password against its hash.
        """

        return self.password_hasher.verify(
            plain_password,
            hashed_password,
        )


# =====================================================
# Password Manager Instance
# =====================================================

password_manager = PasswordManager()


# =====================================================
# OAuth2 Authentication Scheme
# =====================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)
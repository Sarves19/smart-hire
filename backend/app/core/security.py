"""
Security Module

Handles password hashing and verification using Argon2.

This module is responsible for:
- Password hashing
- Password verification
- OAuth2 Bearer Token configuration
"""

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


# Use Passlib's CryptContext with Argon2 for password hashing.
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


class PasswordManager:
    """
    Provides password hashing and verification utilities backed by
    passlib's CryptContext configured for Argon2.
    """

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False


# =====================================================
# Password Manager Instance
# =====================================================

password_manager = PasswordManager()


# =====================================================
# OAuth2 Authentication Scheme
# =====================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
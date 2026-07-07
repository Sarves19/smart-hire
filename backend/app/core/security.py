"""
Security Module

Handles password hashing and verification using Argon2.

This module is responsible ONLY for password security.
JWT generation and validation are handled separately in jwt.py.
"""

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

    def hash_password(self, password: str) -> str:
        """
        Hash a plain text password.

        Args:
            password: User's plain text password.

        Returns:
            Secure Argon2 hashed password.
        """
        return self.password_hasher.hash(password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password: Password entered by the user.
            hashed_password: Password stored in the database.

        Returns:
            True if password matches.
            False otherwise.
        """
        return self.password_hasher.verify(
            plain_password,
            hashed_password,
        )


password_manager = PasswordManager()
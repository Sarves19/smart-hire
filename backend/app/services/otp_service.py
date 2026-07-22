"""
OTP Service

Business logic for generating and verifying one-time-password
codes used for email verification and password reset.
"""

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import password_manager
from app.models.email_verification import EmailVerification, OtpPurpose
from app.repositories.email_verification_repository import (
    EmailVerificationRepository,
)


class OtpService:
    """
    Handles OTP generation, hashing, and verification.
    """

    def __init__(self, db: Session):
        self.repository = EmailVerificationRepository(db)

    # =====================================================
    # GENERATE
    # =====================================================

    def generate_otp(
        self,
        user_id: int,
        purpose: OtpPurpose,
    ) -> str:
        """
        Generate a new numeric OTP, store its hash, and
        invalidate any previous unused OTP for the same
        user/purpose. Returns the PLAIN code so the caller can
        email it - it is never retrievable again after this.
        """

        code = "".join(
            str(secrets.randbelow(10))
            for _ in range(settings.OTP_LENGTH)
        )

        record = EmailVerification(
            user_id=user_id,
            otp_hash=password_manager.hash_password(code),
            purpose=purpose,
            expires_at=datetime.now(timezone.utc)
            + timedelta(minutes=settings.OTP_EXPIRY_MINUTES),
            is_used=False,
            attempts=0,
        )

        # Invalidate and create within one transaction so a concurrent resend
        # cannot leave multiple usable codes behind.
        self.repository.replace_active(record)

        return code

    # =====================================================
    # VERIFY
    # =====================================================

    def verify_otp(
        self,
        user_id: int,
        purpose: OtpPurpose,
        code: str,
    ) -> None:
        """
        Verify a submitted OTP code. Raises ValueError with a
        user-facing message on any failure. Marks the OTP used
        on success so it can't be replayed.
        """

        record = self.repository.get_latest_active(user_id, purpose)

        if record is None:
            raise ValueError(
                "No active verification code found. Please "
                "request a new one."
            )

        if self.repository.is_expired(record):
            raise ValueError(
                "This code has expired. Please request a new one."
            )

        if record.attempts >= settings.OTP_MAX_ATTEMPTS:
            raise ValueError(
                "Too many incorrect attempts. Please request a "
                "new code."
            )

        if not password_manager.verify_password(code, record.otp_hash):
            record.attempts += 1
            self.repository.save(record)

            remaining = settings.OTP_MAX_ATTEMPTS - record.attempts

            if remaining <= 0:
                raise ValueError(
                    "Too many incorrect attempts. Please request "
                    "a new code."
                )

            raise ValueError(
                f"Incorrect code. {remaining} attempt(s) remaining."
            )

        record.is_used = True
        self.repository.save(record)

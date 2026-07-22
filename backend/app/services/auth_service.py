"""
Authentication Service

Contains the business logic for authentication.
"""

import logging
import secrets
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.jwt import jwt_manager
from app.core.security import password_manager
from app.models.email_verification import OtpPurpose
from app.models.user import User, UserRole
from app.models.login_history import LoginHistory, LoginStatus
from app.models.trusted_device import TrustedDevice
from app.repositories.user_repository import UserRepository
from app.repositories.login_history_repository import LoginHistoryRepository
from app.repositories.trusted_device_repository import TrustedDeviceRepository
from sqlalchemy.exc import IntegrityError
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.email_service import email_service
from app.services.otp_service import OtpService

logger = logging.getLogger("smart_hire.auth")

# Keep the user-not-found path as expensive as a normal Argon2 check. This
# avoids giving an attacker a reliable timing signal for registered emails.
DUMMY_PASSWORD_HASH = password_manager.hash_password("not-a-real-password")


class AuthService:
    """
    Handles authentication business logic.
    """

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.otp_service = OtpService(db)
        self.login_history_repository = LoginHistoryRepository(db)
        self.trusted_device_repository = TrustedDeviceRepository(db)

    # =====================================================
    # REGISTER
    # =====================================================

    def register(
        self,
        request: RegisterRequest,
    ) -> User:
        logger.info("register() starting for email=%s", request.email)

        if request.role not in {UserRole.CUSTOMER, UserRole.PROVIDER}:
            logger.warning("register() invalid role=%s", request.role)
            raise ValueError("This role cannot be self-registered.")

        try:
            if self.user_repository.email_exists(request.email):
                logger.warning("register() email_exists=%s", request.email)
                raise ValueError("Email already exists.")

            if self.user_repository.phone_exists(request.phone_number):
                logger.warning("register() phone_exists=%s", request.phone_number)
                raise ValueError("Phone number already exists.")

            logger.info("register() hashing password for email=%s", request.email)
            password_hash = password_manager.hash_password(request.password)
            logger.info("register() password hashed successfully")

            user = User(
                first_name=request.first_name,
                last_name=request.last_name,
                email=request.email,
                phone_number=request.phone_number,
                password_hash=password_hash,
                role=request.role,
                is_active=True,
                is_verified=False,
            )

            logger.info("register() User object created, calling repository.create()")
            user = self.user_repository.create(user)
            logger.info("register() user created with id=%s", user.id)

        except IntegrityError as exc:
            logger.exception("register() IntegrityError: %s", exc)
            msg = "Email or phone number already exists."
            raise ValueError(msg) from exc
        except Exception as exc:
            logger.exception("register() unexpected exception in user creation: %s", exc)
            raise

        # Send the verification OTP. A failure to send email
        # must NOT roll back the newly-created account - the
        # user can always hit /auth/resend-otp. The failure is
        # fully logged inside email_service/email_client.
        try:
            logger.info("register() issuing OTP for user_id=%s", user.id)
            self._issue_and_send_otp(
                user,
                OtpPurpose.EMAIL_VERIFICATION,
                "Email Verification",
            )
            logger.info("register() OTP issued successfully")
        except Exception as exc:
            logger.warning("register() OTP issue failed (non-fatal): %s", exc)

        logger.info("register() completed successfully for user_id=%s", user.id)
        return user


    # =====================================================
    # VERIFY EMAIL (OTP)
    # =====================================================

    def verify_email(self, email: str, otp_code: str) -> dict:

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("User not found.")

        if user.is_verified:
            raise ValueError("Email is already verified.")

        self.otp_service.verify_otp(
            user.id,
            OtpPurpose.EMAIL_VERIFICATION,
            otp_code,
        )

        user.is_verified = True
        user.last_login = datetime.now(timezone.utc)
        self.user_repository.update(user)

        access_token = jwt_manager.create_access_token(subject=str(user.id))
        refresh_token = jwt_manager.create_refresh_token(subject=str(user.id))
        
        # Send welcome email after successful verification
        try:
            email_service.send_welcome_email(user.email, user.first_name)
        except Exception as exc:
            logger.warning("Failed to send welcome email: %s", exc)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.value,
            },
        }

    # =====================================================
    # RESEND VERIFICATION OTP
    # =====================================================

    def resend_verification_otp(self, email: str) -> None:

        user = self.user_repository.get_by_email(email)

        if user is None:
            # Don't reveal whether the email exists.
            return

        if user.is_verified:
            raise ValueError("Email is already verified.")

        self._issue_and_send_otp(
            user,
            OtpPurpose.EMAIL_VERIFICATION,
            "Email Verification",
        )

    # =====================================================
    # FORGOT PASSWORD
    # =====================================================

    def forgot_password(self, email: str) -> None:

        user = self.user_repository.get_by_email(email)

        if user is None:
            # Don't reveal whether the email exists - respond
            # the same way either way at the API layer.
            return

        self._issue_and_send_otp(
            user,
            OtpPurpose.PASSWORD_RESET,
            "Password Reset",
        )

    # =====================================================
    # RESET PASSWORD
    # =====================================================

    def reset_password(
        self,
        email: str,
        otp_code: str,
        new_password: str,
    ) -> None:

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid code.")

        self.otp_service.verify_otp(
            user.id,
            OtpPurpose.PASSWORD_RESET,
            otp_code,
        )

        user.password_hash = password_manager.hash_password(
            new_password
        )
        self.user_repository.update(user)

    # =====================================================
    # INTERNAL HELPER
    # =====================================================

    def _issue_and_send_otp(
        self,
        user: User,
        purpose: OtpPurpose,
        label: str,
    ) -> bool:

        code = self.otp_service.generate_otp(user.id, purpose)

        sent = email_service.send_otp_email(
            to_email=user.email,
            first_name=user.first_name,
            otp_code=code,
            purpose_label=label,
        )

        if not sent:
            logger.warning(
                "OTP generated for user_id=%s purpose=%s but "
                "the email failed to send. User can retry via "
                "/auth/resend-otp.",
                user.id,
                purpose.value,
            )

        return sent

    # =====================================================
    # LOGIN - Simple Email + Password Login
    # =====================================================

    def login(
        self,
        request: LoginRequest,
        ip_address: str | None = None,
        browser: str | None = None,
        operating_system: str | None = None,
        device_fingerprint: str | None = None,
    ) -> dict:
        """
        Simple login with email and password.
        Generates JWT tokens and sends login notification.
        """
        logger.info("login() starting for email=%s", request.email)

        user = self.user_repository.get_by_email(request.email)

        if user is None:
            # Don't reveal whether email exists - run expensive hash check
            password_manager.verify_password(request.password, DUMMY_PASSWORD_HASH)
            logger.warning("login() email not found: %s", request.email)
            raise ValueError("Invalid email or password.")

        # Verify password
        if not password_manager.verify_password(request.password, user.password_hash):
            logger.warning("login() invalid password for email=%s", request.email)
            self._record_login_attempt(
                user,
                LoginStatus.FAILED_INVALID_CREDENTIALS,
                ip_address,
                browser,
                operating_system,
                device_fingerprint,
                failure_reason="Invalid password",
            )
            raise ValueError("Invalid email or password.")

        # Check account status
        if not user.is_active:
            logger.warning("login() account inactive: user_id=%s", user.id)
            self._record_login_attempt(
                user,
                LoginStatus.FAILED_ACCOUNT_INACTIVE,
                ip_address,
                browser,
                operating_system,
                device_fingerprint,
                failure_reason="Account inactive",
            )
            raise ValueError("Account is inactive. Contact support for assistance.")

        if not user.is_verified:
            logger.warning("login() email not verified: user_id=%s", user.id)
            self._record_login_attempt(
                user,
                LoginStatus.FAILED_EMAIL_UNVERIFIED,
                ip_address,
                browser,
                operating_system,
                device_fingerprint,
                failure_reason="Email not verified",
            )
            raise ValueError("Please verify your email address first.")

        # Create tokens
        logger.info("login() generating tokens for user_id=%s", user.id)
        access_token = jwt_manager.create_access_token(subject=str(user.id))
        refresh_token = jwt_manager.create_refresh_token(subject=str(user.id))

        # Update last login timestamp
        user.last_login = datetime.now(timezone.utc)
        self.user_repository.update(user)

        # Record successful login
        login_record = self._record_login_attempt(
            user,
            LoginStatus.SUCCESS,
            ip_address,
            browser,
            operating_system,
            device_fingerprint,
            is_trusted_device=False,
        )

        # Send login notification email (non-blocking)
        try:
            logger.info("login() sending login notification to %s", user.email)
            email_service.send_login_notification(
                to_email=user.email,
                first_name=user.first_name,
                login_time=datetime.now(timezone.utc),
                ip_address=ip_address or "Unknown",
                browser=browser or "Unknown Browser",
                operating_system=operating_system or "Unknown OS",
                device=device_fingerprint[:16] if device_fingerprint else "Web Browser",
                location=None,
                is_new_device=True,
            )
            self.login_history_repository.mark_notification_sent(login_record)
            logger.info("login() notification sent successfully")
        except Exception as exc:
            logger.warning("login() failed to send notification (non-fatal): %s", exc)

        logger.info("login() succeeded for user_id=%s", user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.value,
            },
        }

    # =====================================================
    # LOGIN - Initiate (send OTP)
    # =====================================================

    def login_initiate(
        self,
        email: str,
        ip_address: str | None = None,
    ) -> dict:
        """
        Initiate login by validating email and password,
        then send login OTP to email.
        """
        logger.info("login_initiate() starting for email=%s", email)

        user = self.user_repository.get_by_email(email)

        if user is None:
            # Don't reveal whether email exists
            password_manager.verify_password("dummy", DUMMY_PASSWORD_HASH)
            raise ValueError("Invalid email or password.")

        # Check user status
        if not user.is_active:
            raise ValueError("Account is inactive.")

        if not user.is_verified:
            raise ValueError("Email is not verified. Please verify your email first.")

        # Generate and send login OTP
        try:
            logger.info("login_initiate() generating login OTP for user_id=%s", user.id)
            code = self.otp_service.generate_otp(user.id, OtpPurpose.EMAIL_VERIFICATION)
            
            sent = email_service.send_otp_email(
                to_email=user.email,
                first_name=user.first_name,
                otp_code=code,
                purpose_label="Login Verification",
            )
            
            if not sent:
                logger.warning("Failed to send login OTP for user_id=%s", user.id)
                raise ValueError("Failed to send verification code. Please try again.")
                
            logger.info("login_initiate() completed successfully for user_id=%s", user.id)
            return {
                "message": "Verification code sent to your email",
                "email": user.email,
            }
        except Exception as exc:
            logger.exception("login_initiate() failed: %s", exc)
            raise

    # =====================================================
    # LOGIN - Verify OTP
    # =====================================================

    def login_verify_otp(
        self,
        email: str,
        otp_code: str,
        device_fingerprint: str | None = None,
        device_name: str | None = None,
        browser: str | None = None,
        operating_system: str | None = None,
        ip_address: str | None = None,
        remember_device: bool = False,
    ) -> dict:
        """
        Verify login OTP and issue JWT tokens.
        Optionally remember this device for 30 days.
        """
        logger.info("login_verify_otp() for email=%s", email)

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or OTP.")

        # Verify OTP
        try:
            self.otp_service.verify_otp(
                user.id,
                OtpPurpose.EMAIL_VERIFICATION,
                otp_code,
            )
        except ValueError:
            # Log failed attempt
            self._record_login_attempt(
                user,
                LoginStatus.FAILED_OTP_INVALID,
                ip_address,
                browser,
                operating_system,
                device_fingerprint,
                failure_reason="Invalid OTP",
            )
            raise

        # Create tokens
        access_token = jwt_manager.create_access_token(
            subject=str(user.id)
        )

        refresh_token = jwt_manager.create_refresh_token(
            subject=str(user.id)
        )

        # Handle trusted device
        is_trusted = False
        if remember_device and device_fingerprint:
            try:
                device = TrustedDevice(
                    user_id=user.id,
                    device_fingerprint=device_fingerprint,
                    device_name=device_name or "Remembered Device",
                    browser=browser,
                    operating_system=operating_system,
                    ip_address=ip_address,
                )
                self.trusted_device_repository.create(device)
                is_trusted = True
                logger.info(
                    "Trusted device registered: user_id=%s device=%s",
                    user.id,
                    device_fingerprint[:16],
                )
            except IntegrityError:
                # Device already trusted
                logger.info("Device already trusted: user_id=%s", user.id)
                is_trusted = True
            except Exception as exc:
                logger.warning("Failed to register trusted device: %s", exc)

        # Record successful login
        login_record = self._record_login_attempt(
            user,
            LoginStatus.SUCCESS,
            ip_address,
            browser,
            operating_system,
            device_fingerprint,
            is_trusted_device=is_trusted,
        )

        # Send login notification
        try:
            is_new_device = not is_trusted and device_fingerprint
            email_service.send_login_notification(
                to_email=user.email,
                first_name=user.first_name,
                login_time=datetime.now(timezone.utc),
                ip_address=ip_address,
                browser=browser,
                operating_system=operating_system,
                device=device_name or "Unknown Device",
                location=None,  # Could integrate geolocation here
                is_new_device=is_new_device,
            )
            self.login_history_repository.mark_notification_sent(login_record)
        except Exception as exc:
            logger.warning("Failed to send login notification: %s", exc)

        logger.info("login_verify_otp() succeeded for user_id=%s", user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.value,
            },
        }

    # =====================================================
    # LOGIN - Direct (for trusted devices)
    # =====================================================

    def login_direct(
        self,
        email: str,
        password: str,
        device_fingerprint: str | None = None,
        ip_address: str | None = None,
        browser: str | None = None,
        operating_system: str | None = None,
    ) -> dict | None:
        """
        Allow direct login without OTP if device is trusted.
        Returns tokens if successful, None if OTP required.
        """
        logger.info("login_direct() for email=%s", email)

        user = self.user_repository.get_by_email(email)

        if user is None:
            password_manager.verify_password(password, DUMMY_PASSWORD_HASH)
            raise ValueError("Invalid email or password.")

        # Verify password
        if not password_manager.verify_password(
            password,
            user.password_hash,
        ):
            logger.warning("Invalid password for email=%s", email)
            self._record_login_attempt(
                user,
                LoginStatus.FAILED_INVALID_CREDENTIALS,
                ip_address,
                browser,
                operating_system,
                device_fingerprint,
                failure_reason="Invalid credentials",
            )
            raise ValueError("Invalid email or password.")

        # Check account status
        if not user.is_active:
            self._record_login_attempt(
                user,
                LoginStatus.FAILED_ACCOUNT_INACTIVE,
                ip_address,
                browser,
                device_fingerprint,
                failure_reason="Account inactive",
            )
            raise ValueError("Account is inactive.")

        if not user.is_verified:
            self._record_login_attempt(
                user,
                LoginStatus.FAILED_EMAIL_UNVERIFIED,
                ip_address,
                browser,
                operating_system,
                device_fingerprint,
                failure_reason="Email not verified",
            )
            raise ValueError("Email is not verified.")

        # Check if device is trusted
        is_trusted = False
        if device_fingerprint:
            device = self.trusted_device_repository.get_by_fingerprint(device_fingerprint)
            if device and device.is_valid():
                is_trusted = True
                self.trusted_device_repository.update_last_used(device)
                logger.info("Trusted device login: user_id=%s", user.id)

        # If not trusted, require OTP
        if not is_trusted:
            logger.info("Non-trusted device: requiring OTP for user_id=%s", user.id)
            return None

        # Create tokens
        access_token = jwt_manager.create_access_token(
            subject=str(user.id)
        )

        refresh_token = jwt_manager.create_refresh_token(
            subject=str(user.id)
        )

        # Record successful login
        self._record_login_attempt(
            user,
            LoginStatus.SUCCESS,
            ip_address,
            browser,
            operating_system,
            device_fingerprint,
            is_trusted_device=True,
        )

        logger.info("login_direct() succeeded for user_id=%s (trusted device)", user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.value,
            },
        }

    # =====================================================
    # REFRESH ACCESS TOKEN
    # =====================================================

    def refresh_access_token(
        self,
        refresh_token: str,
    ) -> dict:
        """
        Generate a new access token using a valid refresh token.
        """

        payload = jwt_manager.verify_token(refresh_token)

        if payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token.")

        user_id = payload.get("sub")

        if user_id is None:
            raise ValueError("Invalid refresh token.")

        try:
            user = self.user_repository.get_by_id(int(user_id))
        except (TypeError, ValueError) as exc:
            raise ValueError("Invalid refresh token.") from exc

        if user is None or not user.is_active or not user.is_verified:
            raise ValueError("Invalid refresh token.")

        access_token = jwt_manager.create_access_token(
            subject=str(user.id)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self, user_id: int, device_fingerprint: str | None = None) -> None:
        """
        Log out a user. Optionally deactivate a specific device.
        """
        logger.info("logout() for user_id=%s", user_id)

        if device_fingerprint:
            device = self.trusted_device_repository.get_by_fingerprint(device_fingerprint)
            if device:
                self.trusted_device_repository.deactivate(device)

    # =====================================================
    # HELPER - Record Login Attempt
    # =====================================================

    def _record_login_attempt(
        self,
        user: User,
        status: LoginStatus,
        ip_address: str | None,
        browser: str | None,
        operating_system: str | None,
        device_fingerprint: str | None,
        is_trusted_device: bool = False,
        failure_reason: str | None = None,
    ) -> LoginHistory:
        """Record a login attempt in the database."""
        record = LoginHistory(
            user_id=user.id,
            email=user.email,
            ip_address=ip_address,
            browser=browser,
            operating_system=operating_system,
            device_fingerprint=device_fingerprint,
            status=status,
            is_trusted_device=is_trusted_device,
            failure_reason=failure_reason,
        )
        return self.login_history_repository.create(record)


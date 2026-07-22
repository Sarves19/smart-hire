"""
Authentication API

Provides authentication endpoints.
"""

import logging
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.rate_limit import login_rate_limit, otp_rate_limit

if TYPE_CHECKING:
    from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LogoutRequest,
    LoginRequest,
    LoginVerifyRequest,
    MessageResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    RegisterRequest,
    ResendOtpRequest,
    ResetPasswordRequest,
    TokenResponse,
    VerifyOtpRequest,
)
from app.services.auth_service import AuthService

logger = logging.getLogger("smart_hire.auth")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# =====================================================
# Register
# =====================================================

@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
    _: None = Depends(otp_rate_limit),
):
    """
    Register a new user. Sends an email-verification OTP.
    """
    logger.info("POST /auth/register - request received for email=%s", request.email)

    service = AuthService(db)

    try:
        logger.info("POST /auth/register - calling service.register()")
        service.register(request)
        logger.info("POST /auth/register - service.register() completed successfully")

        return MessageResponse(
            message=(
                "User registered successfully. Please check "
                "your email for a verification code."
            )
        )

    except ValueError as e:
        logger.warning("POST /auth/register - ValueError: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT if "already exists" in str(e) else status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.exception("POST /auth/register - unexpected exception: %s", e)
        raise


# =====================================================
# Verify OTP (email verification)
# =====================================================

@router.post(
    "/verify-otp",
    response_model=TokenResponse,
)
def verify_otp(
    request: VerifyOtpRequest,
    db: Session = Depends(get_db),
    _: None = Depends(otp_rate_limit),
):
    """
    Verify the OTP sent at registration to activate the account.
    """

    service = AuthService(db)

    try:
        token_response = service.verify_email(request.email, request.otp_code)
        return TokenResponse(**token_response)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# Resend OTP
# =====================================================

@router.post(
    "/resend-otp",
    response_model=MessageResponse,
)
def resend_otp(
    request: ResendOtpRequest,
    db: Session = Depends(get_db),
    _: None = Depends(otp_rate_limit),
):
    """
    Resend the email-verification OTP.
    """

    service = AuthService(db)

    try:
        service.resend_verification_otp(request.email)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    # Always return the same message, whether or not the email
    # exists, so this endpoint can't be used to enumerate
    # registered accounts.
    return MessageResponse(
        message="If that email is registered, a new code has been sent."
    )


# =====================================================
# Login - Email + Password
# =====================================================

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
    _: None = Depends(login_rate_limit),
):
    """
    Login with email and password.
    Returns JWT access and refresh tokens.
    Sends login notification email.
    """
    logger.info("POST /auth/login - request received for email=%s", request.email)

    service = AuthService(db)

    try:
        token_response = service.login(
            request=request,
            ip_address=None,  # Could extract from request.client.host
            browser=None,
            operating_system=None,
            device_fingerprint=None,
        )
        
        logger.info("POST /auth/login - login successful for email=%s", request.email)
        return TokenResponse(
            access_token=token_response["access_token"],
            refresh_token=token_response.get("refresh_token"),
            token_type=token_response.get("token_type", "bearer"),
            user=token_response.get("user"),
        )

    except ValueError as e:
        logger.warning("POST /auth/login - login failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except Exception as e:
        logger.exception("POST /auth/login - unexpected error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login.",
        )


# =====================================================
# Forgot Password
# =====================================================

@router.post(
    "/forgot-password",
    response_model=MessageResponse,
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
    _: None = Depends(otp_rate_limit),
):
    """
    Request a password-reset OTP.
    """

    service = AuthService(db)

    service.forgot_password(request.email)

    # Same response regardless of whether the email exists.
    return MessageResponse(
        message="If that email is registered, a reset code has been sent."
    )


# =====================================================
# Reset Password
# =====================================================

@router.post(
    "/reset-password",
    response_model=MessageResponse,
)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
    _: None = Depends(otp_rate_limit),
):
    """
    Reset the password using a verified OTP.
    """

    service = AuthService(db)

    try:
        service.reset_password(
            request.email,
            request.otp_code,
            request.new_password,
        )

        return MessageResponse(
            message="Password reset successfully. You can now log in."
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# Login - Verify OTP
# =====================================================

@router.post(
    "/login-verify",
    response_model=TokenResponse,
)
def login_verify(
    request: LoginVerifyRequest,
    db: Session = Depends(get_db),
    _: None = Depends(otp_rate_limit),
):
    """
    Verify login OTP and return JWT tokens.
    """
    logger.info("POST /auth/login-verify - received for email=%s", request.email)

    service = AuthService(db)

    try:
        token = service.login_verify_otp(
            email=request.email,
            otp_code=request.otp_code,
            device_fingerprint=request.device_fingerprint,
            device_name=request.device_name,
            browser=request.browser,
            operating_system=request.operating_system,
            ip_address=request.ip_address,
            remember_device=request.remember_device,
        )

        logger.info("POST /auth/login-verify - success for email=%s", request.email)
        return TokenResponse(**token)

    except ValueError as e:
        logger.warning("POST /auth/login-verify - verification failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


# =====================================================
# Logout
# =====================================================

@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    request: LogoutRequest,
    current_user: "User" = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Log out a user. Optionally deactivate a specific device.
    Requires authentication.
    """
    logger.info("POST /auth/logout - received for user_id=%s", current_user.id)

    service = AuthService(db)

    try:
        service.logout(current_user.id, request.device_fingerprint)
        logger.info("POST /auth/logout - success for user_id=%s", current_user.id)

        return MessageResponse(message="Logged out successfully.")

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# Refresh Access Token
# =====================================================

@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Generate a new access token using a refresh token.
    """

    service = AuthService(db)

    try:
        token = service.refresh_access_token(
            request.refresh_token
        )

        return RefreshTokenResponse(**token)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

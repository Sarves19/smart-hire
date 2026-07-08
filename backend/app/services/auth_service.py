"""
Authentication Service

Contains the business logic for authentication.
"""

from sqlalchemy.orm import Session

from app.core.jwt import jwt_manager
from app.core.security import password_manager
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:
    """
    Handles authentication business logic.
    """

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    # =====================================================
    # REGISTER
    # =====================================================

    def register(
        self,
        request: RegisterRequest,
    ) -> User:

        if self.user_repository.email_exists(request.email):
            raise ValueError("Email already exists.")

        if self.user_repository.phone_exists(request.phone_number):
            raise ValueError("Phone number already exists.")

        user = User(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone_number=request.phone_number,
            password_hash=password_manager.hash_password(
                request.password
            ),
            role=UserRole(request.role),
            is_active=True,
            is_verified=False,
        )

        return self.user_repository.create(user)

    # =====================================================
    # LOGIN
    # =====================================================

    def login(
        self,
        request: LoginRequest,
    ) -> dict:

        user = self.user_repository.get_by_email(
            request.email
        )

        if user is None:
            raise ValueError("Invalid email or password.")

        if not password_manager.verify_password(
            request.password,
            user.password_hash,
        ):
            raise ValueError("Invalid email or password.")

        access_token = jwt_manager.create_access_token(
            subject=str(user.id)
        )

        refresh_token = jwt_manager.create_refresh_token(
            subject=str(user.id)
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
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

        user = self.user_repository.get_by_id(int(user_id))

        if user is None:
            raise ValueError("User not found.")

        access_token = jwt_manager.create_access_token(
            subject=str(user.id)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
"""
Authentication Dependencies

Provides reusable authentication and authorization dependencies.
"""

from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import jwt_manager
from app.core.security import oauth2_scheme
from app.models.user import User
from app.repositories.user_repository import UserRepository


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Returns the currently authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt_manager.verify_token(token)

        user_id = payload.get("sub")

        if payload.get("type") != "access" or not isinstance(user_id, str):
            raise credentials_exception

        try:
            user_id = int(user_id)
        except ValueError:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Ensures the current user is active.
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user.",
        )

    return current_user


def require_role(*roles):
    """
    Restrict access to specific user roles.
    """

    def role_checker(
        current_user: User = Depends(get_current_active_user),
    ):
        if current_user.role.value not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied.",
            )

        return current_user

    return role_checker

"""
User API

Provides user-related endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# =====================================================
# GET CURRENT USER
# =====================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get the currently authenticated user.
    """

    service = UserService(db)

    return service.get_current_user(current_user)


# =====================================================
# UPDATE CURRENT USER
# =====================================================

@router.put(
    "/me",
    response_model=UserResponse,
)
def update_current_user(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update the currently authenticated user.
    """

    service = UserService(db)

    try:
        return service.update_user(
            current_user,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
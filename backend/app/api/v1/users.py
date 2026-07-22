"""
User API

Provides user-related endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_role
from app.models.user import User, UserRole
from app.schemas.auth import MessageResponse
from app.schemas.user import (
    PasswordChangeRequest,
    UserListResponse,
    UserResponse,
    UserStatusUpdateRequest,
    UserUpdateRequest,
)
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
            status_code=status.HTTP_409_CONFLICT if "already exists" in str(e) else status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/me/change-password", response_model=MessageResponse)
def change_password(
    request: PasswordChangeRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Change the authenticated user's password after current-password verification."""
    try:
        UserService(db).change_password(current_user, request)
        return MessageResponse(message="Password changed successfully.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=UserListResponse)
def list_users(
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    role: UserRole | None = None,
    is_active: bool | None = None,
    _: User = Depends(require_role(UserRole.ADMIN.value)),
    db: Session = Depends(get_db),
):
    """Administratively list users with bounded pagination and filtering."""
    if page < 1 or page_size < 1 or page_size > 100:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid pagination parameters.")
    users, total = UserService(db).list_user_page(page, page_size, search, role, is_active)
    return UserListResponse(items=users, total=total, page=page, page_size=page_size)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    _: User = Depends(require_role(UserRole.ADMIN.value)),
    db: Session = Depends(get_db),
):
    user = UserService(db).get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


@router.patch("/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    request: UserStatusUpdateRequest,
    current_user: User = Depends(require_role(UserRole.ADMIN.value)),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    target_user = service.get_user_by_id(user_id)
    if target_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    try:
        return service.set_account_status(target_user, request.is_active, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

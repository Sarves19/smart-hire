"""
Provider Profile API

Provides endpoints for provider profile management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.user import User, UserRole
from app.schemas.provider import (
    ProviderProfileCreate,
    ProviderProfileResponse,
    ProviderProfileUpdate,
)
from app.services.provider_service import ProviderService

router = APIRouter(
    prefix="/provider",
    tags=["Provider"],
)


# =====================================================
# CREATE PROFILE
# =====================================================

@router.post(
    "/profile",
    response_model=ProviderProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    request: ProviderProfileCreate,
    current_user: User = Depends(
        require_role(UserRole.PROVIDER.value)
    ),
    db: Session = Depends(get_db),
):
    """
    Create provider profile.
    """

    service = ProviderService(db)

    try:
        return service.create_profile(
            current_user,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# GET PROFILE
# =====================================================

@router.get(
    "/profile",
    response_model=ProviderProfileResponse,
)
def get_profile(
    current_user: User = Depends(
        require_role(UserRole.PROVIDER.value)
    ),
    db: Session = Depends(get_db),
):
    """
    Get provider profile.
    """

    service = ProviderService(db)

    try:
        return service.get_profile(current_user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# UPDATE PROFILE
# =====================================================

@router.put(
    "/profile",
    response_model=ProviderProfileResponse,
)
def update_profile(
    request: ProviderProfileUpdate,
    current_user: User = Depends(
        require_role(UserRole.PROVIDER.value)
    ),
    db: Session = Depends(get_db),
):
    """
    Update provider profile.
    """

    service = ProviderService(db)

    try:
        return service.update_profile(
            current_user,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
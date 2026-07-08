"""
Customer Profile API

Provides endpoints for customer profile management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.customer import (
    CustomerProfileCreate,
    CustomerProfileResponse,
    CustomerProfileUpdate,
)
from app.services.customer_service import CustomerService

router = APIRouter(
    prefix="/customer",
    tags=["Customer"],
)


# =====================================================
# CREATE PROFILE
# =====================================================

@router.post(
    "/profile",
    response_model=CustomerProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    request: CustomerProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create customer profile.
    """

    service = CustomerService(db)

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
    response_model=CustomerProfileResponse,
)
def get_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get customer profile.
    """

    service = CustomerService(db)

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
    response_model=CustomerProfileResponse,
)
def update_profile(
    request: CustomerProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update customer profile.
    """

    service = CustomerService(db)

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
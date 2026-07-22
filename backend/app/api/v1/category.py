"""
Category API

Provides endpoints for category management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.user import User, UserRole
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


# =====================================================
# CREATE CATEGORY (ADMIN ONLY)
# =====================================================

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    request: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN.value)
    ),
):
    """
    Create a new category.
    """

    service = CategoryService(db)

    try:
        return service.create_category(request)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# GET CATEGORY (ALL AUTHENTICATED USERS)
# =====================================================

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    """
    Get category by ID.
    """

    service = CategoryService(db)

    try:
        return service.get_category(category_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# LIST CATEGORIES (ALL AUTHENTICATED USERS)
# =====================================================

@router.get(
    "/",
    response_model=list[CategoryResponse],
)
def list_categories(
    db: Session = Depends(get_db),
):
    """
    List all categories.
    """

    service = CategoryService(db)

    return service.list_categories()


# =====================================================
# UPDATE CATEGORY (ADMIN ONLY)
# =====================================================

@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    request: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN.value)
    ),
):
    """
    Update category.
    """

    service = CategoryService(db)

    try:
        return service.update_category(
            category_id,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# DELETE CATEGORY (ADMIN ONLY)
# =====================================================

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN.value)
    ),
):
    """
    Delete category.
    """

    service = CategoryService(db)

    try:
        service.delete_category(category_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
"""
Review API

Provides endpoints for review management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.review import (
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
)
from app.services.review_service import ReviewService

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


# =====================================================
# CREATE REVIEW
# =====================================================

@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    request: ReviewCreate,
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    try:
        return service.create_review(request)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# LIST REVIEWS
# =====================================================

@router.get(
    "/",
    response_model=list[ReviewResponse],
)
def list_reviews(
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    return service.list_reviews()


# =====================================================
# GET REVIEW
# =====================================================

@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    try:
        return service.get_review(review_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# GET PROVIDER REVIEWS
# =====================================================

@router.get(
    "/provider/{provider_id}",
    response_model=list[ReviewResponse],
)
def get_provider_reviews(
    provider_id: int,
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    return service.get_provider_reviews(provider_id)


# =====================================================
# UPDATE REVIEW
# =====================================================

@router.put(
    "/{review_id}",
    response_model=ReviewResponse,
)
def update_review(
    review_id: int,
    request: ReviewUpdate,
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    try:
        return service.update_review(
            review_id,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# DELETE REVIEW
# =====================================================

@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    service = ReviewService(db)

    try:
        service.delete_review(review_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
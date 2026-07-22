"""
Payment API

Provides endpoints for payment management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.payment import PaymentStatus
from app.models.user import UserRole
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentStatusUpdate,
    PaymentUpdate,
)
from app.services.payment_service import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
    dependencies=[Depends(require_role(UserRole.ADMIN.value))],
)


# =====================================================
# CREATE PAYMENT
# =====================================================

@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    request: PaymentCreate,
    db: Session = Depends(get_db),
):
    service = PaymentService(db)

    try:
        return service.create_payment(request)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# LIST PAYMENTS
# =====================================================

@router.get(
    "/",
    response_model=list[PaymentResponse],
)
def list_payments(
    db: Session = Depends(get_db),
):
    service = PaymentService(db)

    return service.list_payments()


# =====================================================
# GET PAYMENT
# =====================================================

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    service = PaymentService(db)

    try:
        return service.get_payment(payment_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# UPDATE PAYMENT
# =====================================================

@router.put(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def update_payment(
    payment_id: int,
    request: PaymentUpdate,
    db: Session = Depends(get_db),
):
    service = PaymentService(db)

    try:
        return service.update_payment(
            payment_id,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# UPDATE PAYMENT STATUS
# =====================================================

@router.patch(
    "/{payment_id}/status",
    response_model=PaymentResponse,
)
def update_status(
    payment_id: int,
    request: PaymentStatusUpdate,
    db: Session = Depends(get_db),
):
    service = PaymentService(db)

    try:
        return service.update_status(
            payment_id,
            PaymentStatus(request.status),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# DELETE PAYMENT
# =====================================================

@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    service = PaymentService(db)

    try:
        service.delete_payment(payment_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

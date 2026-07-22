"""
Booking API

Provides endpoints for booking management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.booking import BookingStatus
from app.models.user import User
from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
    BookingStatusUpdate,
    BookingUpdate,
)
from app.services.booking_service import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


# =====================================================
# CREATE BOOKING
# =====================================================

@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    request: BookingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    service = BookingService(db)

    try:
        return service.create_booking(
            current_user,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# =====================================================
# LIST BOOKINGS
# =====================================================

@router.get(
    "/",
    response_model=list[BookingResponse],
)
def list_bookings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    service = BookingService(db)

    return service.list_bookings(current_user)


# =====================================================
# GET BOOKING
# =====================================================

@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    service = BookingService(db)

    try:
        return service.get_booking(booking_id, current_user)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


# =====================================================
# UPDATE BOOKING
# =====================================================

@router.put(
    "/{booking_id}",
    response_model=BookingResponse,
)
def update_booking(
    booking_id: int,
    request: BookingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    service = BookingService(db)

    try:
        return service.update_booking(
            booking_id,
            request,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# =====================================================
# UPDATE STATUS
# =====================================================

@router.patch(
    "/{booking_id}/status",
    response_model=BookingResponse,
)
def update_status(
    booking_id: int,
    request: BookingStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    service = BookingService(db)

    try:
        return service.update_status(
            booking_id,
            BookingStatus(request.status),
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# =====================================================
# DELETE BOOKING
# =====================================================

@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    service = BookingService(db)

    try:
        service.delete_booking(
            booking_id,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
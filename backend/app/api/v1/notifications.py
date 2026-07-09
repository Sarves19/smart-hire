"""
Notification API

Provides endpoints for notification management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
)
from app.services.notification_service import NotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


# =====================================================
# CREATE NOTIFICATION
# =====================================================

@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    request: NotificationCreate,
    db: Session = Depends(get_db),
):
    service = NotificationService(db)

    try:
        return service.create_notification(request)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# LIST NOTIFICATIONS
# =====================================================

@router.get(
    "/",
    response_model=list[NotificationResponse],
)
def list_notifications(
    db: Session = Depends(get_db),
):
    service = NotificationService(db)

    return service.list_notifications()


# =====================================================
# GET NOTIFICATION
# =====================================================

@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    service = NotificationService(db)

    try:
        return service.get_notification(notification_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# GET USER NOTIFICATIONS
# =====================================================

@router.get(
    "/user/{user_id}",
    response_model=list[NotificationResponse],
)
def get_user_notifications(
    user_id: int,
    db: Session = Depends(get_db),
):
    service = NotificationService(db)

    return service.get_user_notifications(user_id)


# =====================================================
# MARK AS READ
# =====================================================

@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def update_notification(
    notification_id: int,
    request: NotificationUpdate,
    db: Session = Depends(get_db),
):
    service = NotificationService(db)

    try:
        return service.update_notification(
            notification_id,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# DELETE NOTIFICATION
# =====================================================

@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    service = NotificationService(db)

    try:
        service.delete_notification(notification_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
        
        
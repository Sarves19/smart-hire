"""
Service API

Provides endpoints for service management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.user import User, UserRole
from app.schemas.service import (
    ServiceCreate,
    ServiceResponse,
    ServiceUpdate,
)
from app.services.service_service import ServiceService

router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


# =====================================================
# CREATE SERVICE
# =====================================================

@router.post(
    "/",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service(
    request: ServiceCreate,
    current_user: User = Depends(
        require_role(
            UserRole.PROVIDER.value,
            UserRole.ADMIN.value,
        )
    ),
    db: Session = Depends(get_db),
):
    """
    Create a service.
    """

    service = ServiceService(db)

    try:
        return service.create_service(
            current_user,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# LIST SERVICES
# =====================================================

@router.get(
    "/",
    response_model=list[ServiceResponse],
)
def list_services(
    db: Session = Depends(get_db),
):
    """
    List all services.
    """

    service = ServiceService(db)

    return service.list_services()


# =====================================================
# GET SERVICE
# =====================================================

@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
):
    """
    Get service by ID.
    """

    service = ServiceService(db)

    try:
        return service.get_service(service_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# =====================================================
# UPDATE SERVICE
# =====================================================

@router.put(
    "/{service_id}",
    response_model=ServiceResponse,
)
def update_service(
    service_id: int,
    request: ServiceUpdate,
    current_user: User = Depends(
        require_role(
            UserRole.PROVIDER.value,
            UserRole.ADMIN.value,
        )
    ),
    db: Session = Depends(get_db),
):
    """
    Update a service.
    """

    service = ServiceService(db)

    try:
        return service.update_service(
            service_id,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# DELETE SERVICE
# =====================================================

@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_service(
    service_id: int,
    current_user: User = Depends(
        require_role(
            UserRole.PROVIDER.value,
            UserRole.ADMIN.value,
        )
    ),
    db: Session = Depends(get_db),
):
    """
    Delete a service.
    """

    service = ServiceService(db)

    try:
        service.delete_service(service_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    
    
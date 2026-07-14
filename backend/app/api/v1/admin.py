"""
Admin API

Provides endpoints for the admin dashboard.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.user import User, UserRole
from app.schemas.admin import DashboardResponse
from app.services.admin_service import AdminService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


# =====================================================
# Dashboard
# =====================================================

@router.get(
    "/dashboard",
    response_model=DashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN.value)
    ),
):
    """
    Get admin dashboard statistics.
    """

    service = AdminService(db)

    return service.get_dashboard()




from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from dashboard_repository import DashboardRepository
from auth_utils import AuthUtils
from database_config import get_db
from db_models import User

router = APIRouter()

@router.get("/metrics")
async def get_dashboard_metrics(db:AsyncSession = Depends(get_db), current_user: User = Depends(AuthUtils.get_current_user)):
    if current_user.role == "provider":
        metrics = await DashboardRepository.get_provider_metrics(db, current_user.id)
        return metrics
    elif current_user.role == "customer":
        metrics = await DashboardRepository.get_customer_metrics(db, current_user.id)
        return metrics
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user role"
        )
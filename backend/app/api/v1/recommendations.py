"""
Recommendation API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
)
from app.services.recommendation_service import RecommendationService

router = APIRouter(
    prefix="/recommendations",
    tags=["AI Recommendations"],
)


@router.post(
    "/",
    response_model=RecommendationResponse,
)
def recommend(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
):
    """
    Generate AI recommendations.
    """

    service = RecommendationService(db)

    return service.recommend(
        request.query,
    )
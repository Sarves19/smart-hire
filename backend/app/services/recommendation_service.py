"""
Recommendation Service

Coordinates AI recommendations with database data.
"""

from sqlalchemy.orm import Session

from app.ai.recommendation_engine import RecommendationEngine
from app.repositories.recommendation_repository import RecommendationRepository
from app.schemas.recommendation import (
    RecommendationResponse,
    RecommendedProvider,
)


class RecommendationService:
    """
    Service responsible for AI recommendations.
    """

    def __init__(self, db: Session):
        self.repository = RecommendationRepository(db)
        self.engine = RecommendationEngine()

    def recommend(
        self,
        query: str,
    ) -> RecommendationResponse:
        """
        Generate provider recommendations.
        """

        # -------------------------------------------------
        # Check Categories
        # -------------------------------------------------

        categories = self.repository.get_all_categories()

        if not categories:
            return RecommendationResponse(
                query=query,
                success=False,
                message="There are no service categories registered yet.",
                recommendations=[],
            )

        # -------------------------------------------------
        # Check Services
        # -------------------------------------------------

        services = self.repository.get_all_services()

        if not services:
            return RecommendationResponse(
                query=query,
                success=False,
                message="There are no services registered yet.",
                recommendations=[],
            )

        # -------------------------------------------------
        # Check Providers
        # -------------------------------------------------

        providers = self.repository.get_all_providers()

        if not providers:
            return RecommendationResponse(
                query=query,
                success=False,
                message="There are no service providers registered yet.",
                recommendations=[],
            )

        # -------------------------------------------------
        # AI Recommendation
        # -------------------------------------------------

        ai_result = self.engine.recommend(
            query=query,
            providers=providers,
        )

        recommendations = []

        for item in ai_result["recommendations"]:

            provider = item["provider"]

            recommendations.append(
                RecommendedProvider(
                    provider_id=provider.id,
                    provider_name=getattr(
                        provider,
                        "business_name",
                        "Unknown Provider",
                    ),
                    service_name="Service",
                    category="General",
                    rating=float(
                        getattr(provider, "rating", 0)
                    ),
                    match_score=item["score"],
                    reason="Recommended based on AI ranking.",
                    estimated_price=None,
                )
            )

        return RecommendationResponse(
            query=query,
            success=True,
            message="Recommendations generated successfully.",
            recommendations=recommendations,
        )
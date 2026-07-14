"""
Recommendation Schemas

Pydantic models for AI recommendations.
"""

from typing import Optional

from pydantic import BaseModel, Field


# =====================================================
# AI REQUEST
# =====================================================

class RecommendationRequest(BaseModel):
    """
    Customer natural language request.
    """

    query: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Natural language request from customer."
    )


# =====================================================
# RECOMMENDED PROVIDER
# =====================================================

class RecommendedProvider(BaseModel):
    """
    Recommended provider returned by AI.
    """

    provider_id: int

    provider_name: str

    service_name: str

    category: str

    rating: float

    match_score: float

    reason: str

    estimated_price: Optional[float] = None


# =====================================================
# RESPONSE
# =====================================================

class RecommendationResponse(BaseModel):
    """
    Recommendation response.
    """

    query: str

    success: bool

    message: str

    recommendations: list[RecommendedProvider]
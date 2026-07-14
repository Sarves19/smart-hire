"""
Ranking Engine

Calculates provider recommendation scores.
"""

from typing import List


class RankingEngine:
    """
    Scores and ranks providers.
    """

    @staticmethod
    def calculate_score(provider) -> float:
        """
        Calculate recommendation score.
        """

        score = 0.0

        # Rating (40%)
        if hasattr(provider, "rating") and provider.rating:
            score += float(provider.rating) * 8

        # Verified Provider (20%)
        if getattr(provider, "is_verified", False):
            score += 20

        # Active Provider (20%)
        if getattr(provider, "is_active", False):
            score += 20

        # Experience (20%)
        years = getattr(provider, "experience_years", 0)

        score += min(years, 10) * 2

        return round(score, 2)

    @staticmethod
    def rank(providers: List):
        """
        Rank providers from highest to lowest score.
        """

        ranked = []

        for provider in providers:
            ranked.append(
                {
                    "provider": provider,
                    "score": RankingEngine.calculate_score(
                        provider
                    ),
                }
            )

        ranked.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return ranked
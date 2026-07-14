"""
Recommendation Engine

Coordinates the AI recommendation workflow.
"""

from app.ai.llm_service import LLMService
from app.ai.parser import AIResponseParser
from app.ai.prompt_builder import PromptBuilder
from app.ai.ranking_engine import RankingEngine


class RecommendationEngine:
    """
    AI Recommendation Engine.
    """

    def __init__(self):
        self.llm = LLMService()

    def analyze_query(
        self,
        query: str,
    ) -> dict:
        """
        Convert a natural language query into structured data.
        """

        prompt = PromptBuilder.build_recommendation_prompt(
            query
        )

        ai_response = self.llm.extract_user_intent(
            prompt
        )

        return AIResponseParser.parse(
            ai_response
        )

    def recommend(
        self,
        query: str,
        providers: list,
    ) -> dict:
        """
        Return AI recommendations.
        """

        intent = self.analyze_query(query)

        ranked = RankingEngine.rank(
            providers
        )

        return {
            "intent": intent,
            "recommendations": ranked[:5],
        }
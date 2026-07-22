"""
LLM Service

Handles communication with the Large Language Model.
"""

import json

from openai import OpenAI

from app.core.config import settings


class LLMService:
    """
    Handles AI requests.
    """

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

    def extract_user_intent(
        self,
        prompt: str,
    ) -> dict:
        """
        Extract structured information from a natural language request.
        """

        response = self.client.chat.completions.create(
            model=settings.OPENROUTER_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant that extracts structured data. "
                        "Always respond with valid JSON only."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            max_tokens=300,
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise ValueError(
                f"LLM returned invalid JSON:\n{content}"
            )
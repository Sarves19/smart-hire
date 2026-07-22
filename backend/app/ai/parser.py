"""
Parser

Parses and validates AI responses.
"""

from typing import Any


class AIResponseParser:
    """
    Parses AI responses into structured data.
    """

    REQUIRED_FIELDS = [
        "category",
        "location",
        "date",
        "skill",
        "additional_requirements",
    ]

    @staticmethod
    def parse(response: dict[str, Any]) -> dict[str, Any]:
        """
        Ensure all expected keys exist.
        """

        parsed = {}

        for field in AIResponseParser.REQUIRED_FIELDS:
            parsed[field] = response.get(field)

        return parsed
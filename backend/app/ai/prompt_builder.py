"""
Prompt Builder

Builds prompts for the LLM.
"""


class PromptBuilder:

    @staticmethod
    def build_recommendation_prompt(
        query: str,
    ) -> str:

        return f"""
You are an AI assistant for Smart Hire.

Customer Request:

{query}

Your job is to identify:

- Category
- Required Skill
- Preferred Time
- Location
- Additional Requirements

Respond ONLY in JSON.
"""
    
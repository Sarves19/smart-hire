"""
Standard API Responses

Provides reusable response models for the entire application.
"""

from typing import Any

from pydantic import BaseModel


class APIResponse(BaseModel):
    """
    Standard API response.
    """

    success: bool
    message: str
    data: Any | None = None


class SuccessResponse(APIResponse):
    """
    Success response.
    """

    success: bool = True


class ErrorResponse(APIResponse):
    """
    Error response.
    """

    success: bool = False

    
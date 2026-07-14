"""
Global Exception Handlers

Registers custom exception handlers for FastAPI.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.exceptions import AppException


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all application exception handlers.
    """

    # =====================================================
    # Custom Application Exceptions
    # =====================================================

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
            },
        )

    # =====================================================
    # Pydantic Validation Errors
    # =====================================================

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: ValidationError,
    ):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation failed.",
                "errors": exc.errors(),
            },
        )

    # =====================================================
    # Unexpected Exceptions
    # =====================================================

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
                "error": str(exc),
            },
        )
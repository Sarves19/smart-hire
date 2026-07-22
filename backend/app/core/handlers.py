"""
Global Exception Handlers

Registers custom exception handlers for FastAPI.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.exceptions import AppException

logger = logging.getLogger("smart_hire.errors")


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
        # Let FastAPI/Starlette handle HTTPExceptions (preserve their status)
        from fastapi import HTTPException
        if isinstance(exc, HTTPException):
            raise exc

        # Log with the exception traceback and full details
        logger.exception(
            "Unhandled exception while processing %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )

        # Preserve CORS response headers for browsers by echoing the Origin
        headers = {}
        origin = request.headers.get("origin")
        allowed = getattr(__import__("app.core.config", fromlist=["settings"]), "settings").CORS_ORIGINS
        if origin and origin in allowed:
            headers["Access-Control-Allow-Origin"] = origin
            headers["Vary"] = "Origin"

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
            },
            headers=headers,
        )

"""
Smart Hire Application Entry Point
"""

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.api.v1 import (
    admin_router,
    auth_router,
    bookings_router,
    category_router,
    customer_router,
    notifications_router,
    payments_router,
    provider_router,
    recommendations_router,
    reviews_router,
    service_router,
    users_router,
)
from app.core.config import settings
from app.core.handlers import register_exception_handlers

logger = logging.getLogger("smart_hire.main")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="AI-Powered Service Marketplace",
)

# =====================================================
# CORS Configuration
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Security Headers Middleware
# =====================================================

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add browser security headers while allowing FastAPI Swagger UI."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # General security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        # Allow Swagger UI assets
        if request.url.path.startswith("/docs") or \
           request.url.path.startswith("/redoc") or \
           request.url.path.startswith("/openapi.json"):

            response.headers["Content-Security-Policy"] = (
                "default-src 'self' https://cdn.jsdelivr.net https://fastapi.tiangolo.com; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https://fastapi.tiangolo.com; "
                "font-src 'self' https://cdn.jsdelivr.net; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self';"
            )
        else:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "object-src 'none'; "
                "frame-ancestors 'none'; "
                "base-uri 'self';"
            )

        if settings.APP_ENV.lower() == "production":
            response.headers[
                "Strict-Transport-Security"
            ] = "max-age=31536000; includeSubDomains"

        return response


app.add_middleware(SecurityHeadersMiddleware)

# =====================================================
# Static Files
# =====================================================

uploads_directory = Path(__file__).resolve().parent.parent / "uploads"
uploads_directory.mkdir(parents=True, exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=str(uploads_directory)),
    name="uploads",
)

# =====================================================
# Register Global Exception Handlers
# =====================================================

register_exception_handlers(app)

# =====================================================
# API Routers
# =====================================================

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(customer_router, prefix="/api/v1")
app.include_router(provider_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(service_router, prefix="/api/v1")
app.include_router(bookings_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
app.include_router(reviews_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(recommendations_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")

# =====================================================
# Startup Event
# =====================================================

@app.on_event("startup")
async def startup_event():
    """Log configuration status on startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} ({settings.APP_ENV})")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Log email configuration status
    if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
        logger.info(
            f"Email (SMTP) configured: {settings.SMTP_USERNAME} "
            f"(host={settings.SMTP_HOST}:{settings.SMTP_PORT}, "
            f"ssl={settings.SMTP_USE_SSL}). "
            "OTP emails, login notifications, and password reset emails are ENABLED."
        )
    else:
        logger.warning(
            "Email (SMTP) not configured. Set SMTP_USERNAME and SMTP_PASSWORD in .env "
            "to enable email features: registration OTP, login OTP, login notifications, "
            "password reset. Using Gmail? Ensure SMTP_PASSWORD is your 16-character "
            "App Password (not your regular password)."
        )
    
    logger.info("Application startup complete.")

# =====================================================
# Root Endpoint
# =====================================================

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }


# =====================================================
# Health Check
# =====================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }
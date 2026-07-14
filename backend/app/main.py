"""
Smart Hire Application Entry Point
"""

from fastapi import FastAPI

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

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="AI-Powered Service Marketplace",
)

# =====================================================
# Register Global Exception Handlers
# =====================================================

register_exception_handlers(app)

# =====================================================
# API Routers
# =====================================================

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    users_router,
    prefix="/api/v1",
)

app.include_router(
    customer_router,
    prefix="/api/v1",
)

app.include_router(
    provider_router,
    prefix="/api/v1",
)

app.include_router(
    category_router,
    prefix="/api/v1",
)

app.include_router(
    service_router,
    prefix="/api/v1",
)

app.include_router(
    bookings_router,
    prefix="/api/v1",
)

app.include_router(
    payments_router,
    prefix="/api/v1",
)

app.include_router(
    reviews_router,
    prefix="/api/v1",
)

app.include_router(
    notifications_router,
    prefix="/api/v1",
)

app.include_router(
    recommendations_router,
    prefix="/api/v1",
)

app.include_router(
    admin_router,
    prefix="/api/v1",
)

# =====================================================
# Root Endpoint
# =====================================================

@app.get("/")
def root():
    """
    Root endpoint.
    """
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
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }


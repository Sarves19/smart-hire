"""
Smart Hire Application Entry Point
"""

from fastapi import FastAPI

from app.api.v1 import (
    auth_router,
    category_router,
    customer_router,
    provider_router,
    service_router,
    users_router,
)
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="AI-Powered Service Marketplace",
)

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
    }

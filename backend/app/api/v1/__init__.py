"""
API Version 1

Exports all API routers.
"""

from app.api.v1.admin import router as admin_router
from app.api.v1.auth import router as auth_router
from app.api.v1.bookings import router as bookings_router
from app.api.v1.category import router as category_router
from app.api.v1.customer import router as customer_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.payments import router as payments_router
from app.api.v1.provider import router as provider_router
from app.api.v1.recommendations import router as recommendations_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.service import router as service_router
from app.api.v1.users import router as users_router

__all__ = [
    "auth_router",
    "users_router",
    "customer_router",
    "provider_router",
    "category_router",
    "service_router",
    "bookings_router",
    "payments_router",
    "reviews_router",
    "notifications_router",
    "recommendations_router",
    "admin_router",
]

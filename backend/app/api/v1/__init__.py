"""
API Version 1
"""

from app.api.v1.auth import router as auth_router
from app.api.v1.category import router as category_router
from app.api.v1.customer import router as customer_router
from app.api.v1.provider import router as provider_router
from app.api.v1.service import router as service_router
from app.api.v1.users import router as users_router

__all__ = [
    "auth_router",
    "users_router",
    "customer_router",
    "provider_router",
    "category_router",
    "service_router",
]

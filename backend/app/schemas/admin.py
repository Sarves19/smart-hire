"""
Admin Schemas

Pydantic models for admin dashboard.
"""

from pydantic import BaseModel


# =====================================================
# Dashboard Statistics
# =====================================================

class DashboardStatistics(BaseModel):
    """
    Dashboard statistics response.
    """

    total_users: int

    total_customers: int

    total_providers: int

    total_categories: int

    total_services: int

    total_bookings: int

    total_payments: int

    total_reviews: int


# =====================================================
# Dashboard Response
# =====================================================

class DashboardResponse(BaseModel):
    """
    Admin dashboard response.
    """

    success: bool

    message: str

    statistics: DashboardStatistics
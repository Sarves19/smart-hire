"""
Admin Service

Business logic for the admin dashboard.
"""

from sqlalchemy.orm import Session

from app.repositories.admin_repository import AdminRepository
from app.schemas.admin import (
    DashboardResponse,
    DashboardStatistics,
)


class AdminService:
    """
    Service responsible for admin operations.
    """

    def __init__(self, db: Session):
        self.repository = AdminRepository(db)

    # =====================================================
    # Dashboard
    # =====================================================

    def get_dashboard(self) -> DashboardResponse:
        """
        Get dashboard statistics.
        """

        statistics = self.repository.get_dashboard_statistics()

        return DashboardResponse(
            success=True,
            message="Dashboard statistics retrieved successfully.",
            statistics=DashboardStatistics(
                total_users=statistics["total_users"],
                total_customers=statistics["total_customers"],
                total_providers=statistics["total_providers"],
                total_categories=statistics["total_categories"],
                total_services=statistics["total_services"],
                total_bookings=statistics["total_bookings"],
                total_payments=statistics["total_payments"],
                total_reviews=statistics["total_reviews"],
            ),
        )
    
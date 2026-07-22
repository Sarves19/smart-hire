"""
Admin Repository

Provides database operations for the admin dashboard.
"""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.customer_profile import CustomerProfile
from app.models.provider_profile import ProviderProfile
from app.models.category import Category
from app.models.service import Service
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.review import Review


class AdminRepository:
    """
    Repository responsible for admin database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # Dashboard Statistics
    # =====================================================

    def get_dashboard_statistics(self) -> dict:
        """
        Get dashboard statistics.
        """

        total_users = self.db.scalar(
            select(func.count(User.id))
        ) or 0

        total_customers = self.db.scalar(
            select(func.count(CustomerProfile.id))
        ) or 0

        total_providers = self.db.scalar(
            select(func.count(ProviderProfile.id))
        ) or 0

        total_categories = self.db.scalar(
            select(func.count(Category.id))
        ) or 0

        total_services = self.db.scalar(
            select(func.count(Service.id))
        ) or 0

        total_bookings = self.db.scalar(
            select(func.count(Booking.id))
        ) or 0

        total_payments = self.db.scalar(
            select(func.count(Payment.id))
        ) or 0

        total_reviews = self.db.scalar(
            select(func.count(Review.id))
        ) or 0

        return {
            "total_users": total_users,
            "total_customers": total_customers,
            "total_providers": total_providers,
            "total_categories": total_categories,
            "total_services": total_services,
            "total_bookings": total_bookings,
            "total_payments": total_payments,
            "total_reviews": total_reviews,
        }
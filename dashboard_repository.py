from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db_models import Booking, Review


class DashboardRepository:

    @staticmethod
    async def get_customer_metrics(db:AsyncSession, customer_id: int):
        query = select(Booking).where(Booking.customer_id == customer_id)
        result = await db.execute(query)
        bookings = result.scalars().all()

        metrics = {
            "total_bookings": len(bookings),
            "pending_bookings":sum(1 for b in  bookings if b.status == "pending"),
            "accepted_bookings": sum(1 for b in bookings if b.status == "accepted"),
            "completed_bookings": sum(1 for b in bookings if b.status == "completed"),
            "rejected_bookings": sum(1 for b in bookings if b.status == "rejected"),
        }
        return metrics

    @staticmethod
    async def get_provider_metrics(db:AsyncSession, provider_id:int):
        query_bookings = select(Booking).where(Booking.provider_id == provider_id)
        res_bookings = await db.execute(query_bookings)
        bookings = res_bookings.scalars().all()

        query_reviews = select(
            func.count(Review.id).label("total_reviews"),
            func.avg(Review.rating).label("average_rating")
        ).where(Review.provider_id == provider_id)

        res_reviews = await db.execute(query_reviews)
        review_stats = res_reviews.first()

        metrics = {
            "total_bookings": len(bookings),
            "pending_bookings": sum(1 for b in bookings if b.status == "pending"),
            "accepted_bookings": sum(1 for b in bookings if b.status == "accepted"),
            "completed_bookings": sum(1 for b in bookings if b.status == "completed"),
            "rejected_bookings": sum(1 for b in bookings if b.status == "rejected"),
            "average_rating": round(review_stats.average_rating or 0.0,2),
            "total_reviews": review_stats.total_reviews or 0

        }
        return metrics
"""
Review Repository

Handles all database operations related to reviews.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.review import Review
from app.models.service import Service


class ReviewRepository:
    """
    Repository responsible for review operations.
    """

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        review: Review,
    ) -> Review:
        """
        Create a new review.
        """

        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        return review

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(
        self,
        review_id: int,
    ) -> Optional[Review]:
        """
        Get review by ID.
        """

        stmt = select(Review).where(
            Review.id == review_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_by_booking(
        self,
        booking_id: int,
    ) -> Optional[Review]:
        """
        Get review by booking.
        """

        stmt = select(Review).where(
            Review.booking_id == booking_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()

    def get_provider_reviews(
        self,
        provider_id: int,
    ) -> list[Review]:
        """
        Return all reviews for a provider (joined through the
        reviewed service).
        """

        stmt = (
            select(Review)
            .join(Service, Review.service_id == Service.id)
            .where(Service.provider_id == provider_id)
        )

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    def list_reviews(self) -> list[Review]:
        """
        Return all reviews.
        """

        stmt = select(Review)

        result = self.db.execute(stmt)

        return list(result.scalars().all())

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        review: Review,
    ) -> Review:
        """
        Update review.
        """

        self.db.commit()
        self.db.refresh(review)

        return review

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        review: Review,
    ) -> None:
        """
        Delete review.
        """

        self.db.delete(review)
        self.db.commit()
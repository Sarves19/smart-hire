"""
Review Service

Contains business logic for review management.
"""

from sqlalchemy.orm import Session

from app.models.review import Review
from app.repositories.booking_repository import BookingRepository
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
)


class ReviewService:
    """
    Handles review business logic.
    """

    def __init__(self, db: Session):
        self.review_repository = ReviewRepository(db)
        self.booking_repository = BookingRepository(db)

    # =====================================================
    # CREATE REVIEW
    # =====================================================

    def create_review(
        self,
        request: ReviewCreate,
    ) -> Review:
        """
        Create a review.
        """

        booking = self.booking_repository.get_by_id(
            request.booking_id
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        existing_review = self.review_repository.get_by_booking(
            request.booking_id
        )

        if existing_review:
            raise ValueError(
                "Review already exists for this booking."
            )

        review = Review(
            booking_id=booking.id,
            customer_id=booking.customer_id,
            provider_id=booking.provider_id,
            rating=request.rating,
            comment=request.comment,
        )

        return self.review_repository.create(review)

    # =====================================================
    # GET REVIEW
    # =====================================================

    def get_review(
        self,
        review_id: int,
    ) -> Review:

        review = self.review_repository.get_by_id(
            review_id
        )

        if review is None:
            raise ValueError(
                "Review not found."
            )

        return review

    # =====================================================
    # LIST REVIEWS
    # =====================================================

    def list_reviews(self) -> list[Review]:

        return self.review_repository.list_reviews()

    # =====================================================
    # GET PROVIDER REVIEWS
    # =====================================================

    def get_provider_reviews(
        self,
        provider_id: int,
    ) -> list[Review]:

        return self.review_repository.get_provider_reviews(
            provider_id
        )

    # =====================================================
    # UPDATE REVIEW
    # =====================================================

    def update_review(
        self,
        review_id: int,
        request: ReviewUpdate,
    ) -> Review:

        review = self.review_repository.get_by_id(
            review_id
        )

        if review is None:
            raise ValueError(
                "Review not found."
            )

        if request.rating is not None:
            review.rating = request.rating

        if request.comment is not None:
            review.comment = request.comment

        return self.review_repository.update(
            review
        )

    # =====================================================
    # DELETE REVIEW
    # =====================================================

    def delete_review(
        self,
        review_id: int,
    ) -> None:

        review = self.review_repository.get_by_id(
            review_id
        )

        if review is None:
            raise ValueError(
                "Review not found."
            )

        self.review_repository.delete(review)
        
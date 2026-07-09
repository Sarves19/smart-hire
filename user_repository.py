import datetime
import logging
from http.client import HTTPException
from typing import Union, Optional
from auth_utils import AuthUtils
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from db_models import User, Provider, Review
from resp_models import UserResponse, CustomerCreate, ProviderCreate, ReviewCreate, ProviderUpdate

logger = logging.getLogger("smart_hire_logger")
logging.basicConfig(level=logging.INFO)


class UserRepository():

    @staticmethod
    async def create_user(db:AsyncSession, user_data:Union[CustomerCreate, ProviderCreate])-> UserResponse:

        print(user_data.password)
        print(type(user_data.password))
        print(len(user_data.password.encode("utf-8")))

        hashed_password = AuthUtils.hash_password(user_data.password)

        db_user= User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            role=user_data.role
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        if user_data.role == "provider" and user_data.service_type:
            db_provider= Provider(
                service_type=user_data.service_type,
                experience_years=user_data.experience_years,
                hourly_rate=user_data.hourly_rate,
                location=user_data.location,
                is_available=True,
                rating=0.0,
                user_id=db_user.id
            )
            db.add(db_provider)
            await db.commit()
        await db.refresh(db_user, attribute_names=["provider_profile"])

        return db_user

    @staticmethod
    async def get_user_by_email(db: AsyncSession,email:str) -> User | None:
        query = select(User).where(User.email == email).options(joinedload(User.provider_profile))
        result = await db.execute(query)
        return result.scalar_one_or_none()



class ReviewRepository:

    @staticmethod
    async def create_review(db:AsyncSession, review_data: ReviewCreate, customer_id: int):
        db_review = Review(
            rating=review_data.rating,
            comment=review_data.comment,
            provider_id=review_data.provider_id,
            customer_id=customer_id,
            review_date=review_data.review_date,
        )
        db.add(db_review)
        await db.commit()
        await db.refresh(db_review)

        avg_rating_query = select(func.avg(Review.rating).filter(Review.provider_id == review_data.provider_id))
        result = await db.execute(avg_rating_query)
        avg_rating = result.scalar()

        if avg_rating is not None:
            provider_query = select(Provider).where(Provider.id == review_data.provider_id)
            provider_result = await db.execute(provider_query)
            provider = provider_result.scalar()

            if provider:
                provider.rating = round(float(avg_rating),2)
                await db.commit()

        return db_review

    @staticmethod
    async def get_reviews_for_provider(db:AsyncSession,provider_id: int):
        query = select(Review).where(Review.provider_id == provider_id)
        result = await db.execute(query)
        return result.scalars().all()
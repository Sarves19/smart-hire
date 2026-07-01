import logging
from typing import Union
from auth_utils import AuthUtils
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from db_models import User, Provider
from resp_models import UserResponse, CustomerCreate, ProviderCreate

logger = logging.getLogger("smart_hire_logger")
logging.basicConfig(level=logging.INFO)


class UserRepository():

    async def create_user(self, db:AsyncSession, user_data:Union[CustomerCreate, ProviderCreate])-> UserResponse:

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


    async def get_user_by_email(self, db: AsyncSession,email:str) -> User | None:
        query = select(User).where(User.email == email).options(joinedload(User.provider_profile))
        result = await db.execute(query)
        return result.scalar_one_or_none()



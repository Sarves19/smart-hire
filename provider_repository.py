from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db_models import Provider
from resp_models import ProviderUpdate


class ProviderRepository:

    @staticmethod
    async def get_all_providers(db: AsyncSession, service_type: str = None, location: str = None):
        query = select(Provider).options(joinedload(Provider.user))

        if service_type:
            query = query.where(Provider.service_type.ilike(f"%{service_type}"))

        if location:
            query = query.where(Provider.location.ilike(f"%{location}"))
        result = await db.execute(query)
        providers = result.scalars().all()

        provider_list = []
        for p in providers:
            user_name_val = p.user.username if p.user else "Unknown User"

            provider_list.append({
                "id": p.id,
                "user_id": p.user_id,
                "user_name": user_name_val,
                "service_type": p.service_type,
                "experience_years": p.experience_years,
                "hourly_rate": p.hourly_rate,
                "location": p.location,
                "is_available": p.is_available,
                "rating": p.rating
            })
        return provider_list

    @staticmethod
    async def update_provider_listing(db: AsyncSession, user_id: int, update_data: ProviderUpdate):
        query = select(Provider).where(Provider.id == user_id)
        result = await db.execute(query)
        provider = result.scalar()

        if not provider:
            raise HTTPException(
                status_code=404,
                detail="Provider profile not found."
            )
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(provider, key, value)

        await db.commit()
        await db.refresh(provider)
        return provider

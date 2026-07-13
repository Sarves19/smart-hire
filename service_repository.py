from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db_models import Service
from resp_models import ServiceUpdate


class ServiceRepository:

    @staticmethod
    async def get_all_services(db:AsyncSession, skip: int = 0, limit: int = 100):
        query = await db.execute(select(Service).offset(skip).limit(limit))
        return query.scalars().all()

    @staticmethod
    async def get_service_by_id(db:AsyncSession, service_id: int):
        query = await db.execute(select(Service).where(Service.service_id == service_id))
        service = query.scalars().first()
        if not service:
            raise HTTPException(
                status_code=404,
                detail="Service not found."
            )
        return service

    @staticmethod
    async def update_service(db:AsyncSession, service_id: int, service_data: ServiceUpdate):
        service = await ServiceRepository.get_service_by_id(db, service_id)
        update_data = service_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(service, key, value)

        await db.commit()
        await db.refresh(service)
        return service

    @staticmethod
    async def delete_service(db:AsyncSession, service_id: int):
        service = await ServiceRepository.get_service_by_id(db,service_id)
        await db.delete(service)
        await db.commit()
        return {"message": "Service deleted successfully"}

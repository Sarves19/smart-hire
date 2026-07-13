from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database_config import get_db
from resp_models import ServiceResponse, ServiceUpdate
from service_repository import ServiceRepository

router = APIRouter()
service_repo = ServiceRepository()

@router.get("/",response_model=List[ServiceResponse])
async def read_services(skip: int = 0, limit: int = 100, db:AsyncSession = Depends(get_db)):
    return await service_repo.get_all_services(db, skip=skip, limit=limit)

@router.get("/{service_id}",response_model=ServiceResponse)
async def read_service(service_id: int, db:AsyncSession = Depends(get_db)):
    return await service_repo.get_service_by_id(db,service_id)

@router.put("/{service_id}",response_model=ServiceResponse)
async def update_service(service_id:int,service_data:ServiceUpdate, db:AsyncSession = Depends(get_db)):
    await service_repo.update_service(db, service_id, service_data)

@router.delete("/{service_id}")
async def delete_service(service_id: int, db:AsyncSession = Depends(get_db)):
    return await service_repo.delete_service(db, service_id)
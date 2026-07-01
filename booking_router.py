from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from booking_repository import BookingRepository
from database_config import get_db
from resp_models import BookingResponse, BookingCreate

router = APIRouter()
booking_repo = BookingRepository()

@router.post("/create", response_model=BookingResponse, status_code=HTTP_201_CREATED)
async def create_new_booking(booking: BookingCreate, db:AsyncSession = Depends(get_db)):
    new_booking = await booking_repo.create_booking(db,booking)
    return new_booking
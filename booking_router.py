from typing import List
from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database_config import get_db
from db_models import User
from resp_models import BookingResponse, BookingCreate
from booking_repository import BookingRepository
import auth_utils
router = APIRouter()


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_new_booking(booking_data: BookingCreate, db:AsyncSession = Depends(get_db), current_user: User = Depends(auth_utils.AuthUtils.get_current_user)):
   if current_user.role != "customer":
       raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN,
           detail="Providers can't create bookings,Please login as a customer."
       )
   return await BookingRepository.create_booking(db, booking_data,current_user.id)

@router.get("/", response_model=List[BookingResponse])
async def get_my_bookings(db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_utils.AuthUtils.get_current_user)):
    return await BookingRepository.get_user_bookings(db, user_id=current_user.id,role=current_user.role)


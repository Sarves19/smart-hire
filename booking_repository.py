from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Booking
from resp_models import BookingCreate


class BookingRepository:
    async def create_booking(self, db:AsyncSession, booking_data: BookingCreate):
        db_booking = Booking(
            job_title = booking_data.job_title,
            description = booking_data.description,
            user_id = booking_data.user_id
        )
        db.add(db_booking)
        await db.commit()
        await db.refresh(db_booking)
        return db_booking
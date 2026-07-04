from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db_models import Booking
from resp_models import BookingCreate


class BookingRepository:

    @staticmethod
    async def create_booking(db:AsyncSession, booking_data: BookingCreate, customer_id: int):
        new_booking = Booking(
            job_title=booking_data.job_title,
            description=booking_data.description,
            provider_id=booking_data.provider_id,
            customer_id=customer_id,
            booking_date=booking_data.booking_date,
        )
        db.add(new_booking)
        await db.commit()
        await db.refresh(new_booking)
        return new_booking

    @staticmethod
    async def get_user_bookings(db:AsyncSession, user_id: int, role: str):
        if role == "provider":
            query = select(Booking).where(Booking.provider_id == user_id)
        else:
            query = select(Booking).where(Booking.customer_id == user_id)

        result = await db.execute(query)
        return result.scalars().all()
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db_models import Booking, Provider
from resp_models import BookingCreate


class BookingRepository:

    @staticmethod
    async def create_booking(db: AsyncSession,booking_data: BookingCreate,current_user_id: int):
        provider = await db.get(Provider, booking_data.provider_profile_id)

        if provider is None:
            raise HTTPException(
                status_code=404,
                detail="Provider not found"
            )

        new_booking = Booking(
            job_title=booking_data.job_title,
            description=booking_data.description,
            customer_id=current_user_id,
            provider_id=provider.user_id,
            status="pending",
            booking_date=booking_data.booking_date
        )

        db.add(new_booking)
        await db.commit()
        await db.refresh(new_booking)

        return new_booking

    @staticmethod
    async def get_user_bookings(db:AsyncSession, user_id: int, role: str):
        print("======= GET USER BOOKINGS======")
        print("Role",role)
        print("Current User ID", user_id)

        if role == "provider":
            print("Searching by provider_id")
            query = select(Booking).where(Booking.provider_id == user_id)
        else:
            print("Searching by customer_id")
            query = select(Booking).where(Booking.customer_id == user_id)

        result = await db.execute(query)
        bookings = result.scalars().all()

        print("Booking Found:", len(bookings))

        for booking in bookings:
            print(
                "Booking ID: ",booking.id,
                "| Customer ID: ",booking.customer_id,
                "| Provider ID: ", booking.provider_id
            )

        print("==============================================")

        return bookings

    @staticmethod
    async def update_booking_status(db:AsyncSession, booking_id:int, new_status:str, provider_id:int):
        query = select(Booking).where(Booking.id == booking_id,Booking.provider_id == provider_id)
        result = await db.execute(query)
        booking = result.scalar()

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found or you are not authorized to update this booking."
            )

        booking.status = new_status

        await db.commit()
        await db.refresh(booking)
        return booking


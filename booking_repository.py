import asyncio

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db_models import Booking, Provider, Notification
from notification_router import NotificationWebSocketManager
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
            provider_id=provider.id,
            status="pending",
            booking_date=booking_data.booking_date
        )

        db.add(new_booking)
        await db.flush()

        new_notification = Notification(
            user_id=provider.user_id,
            message=f"You have received a new booking request for '{new_booking.job_title}' (Booking ID: #{new_booking.id}.) ",
            type="Booking_Request"
        )
        db.add(new_notification)

        await db.commit()
        await db.refresh(new_booking)
        await db.refresh(new_notification)

        live_payload = {
            "notification_id": new_notification.notification_id,
            "message": f"You have a new booking request for '{new_booking.job_title}'!",
            "type": "New Booking_Received",
            "is_read": False
        }

        asyncio.create_task(
            NotificationWebSocketManager.send_personal_notification(
                user_id=new_booking.provider_id,
                message=live_payload
            )
        )


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
        query = select(Booking).where(Booking.id == booking_id)
        result = await db.execute(query)
        booking = result.scalar()

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found or you are not authorized to update this booking."
            )

        booking.status = new_status
        await db.flush()

        if new_status.lower() == "accepted":
            msg = f"Your booking request for '{booking.job_title}' has been ACCEPTED by the provider! (Booking ID: #{booking.id})."
            notif_type = "Booking_Accepted"
        elif new_status.lower() == "rejected":
            msg = f"Your booking request for '{booking.job_title}' has been REJECTED by the provider! (Booking ID: #{booking.id})."
            notif_type = "Booking_Rejected"
        else:
            msg = f"Your booking status for '{booking.job_title} has been updated to '{new_status}."
            notif_type = "Booking_Updated"

        new_notification = Notification(
            user_id=booking.customer_id,
            message=msg,
            type=notif_type
        )
        db.add(new_notification)
        await db.commit()
        await db.refresh(booking)

        live_payload = {
            "notification_id": new_notification.notification_id,
            "message":msg,
            "type":notif_type,
            "is_read":False
        }

        asyncio.create_task(
            NotificationWebSocketManager.send_personal_notification(
                user_id=booking.customer_id,
                message=live_payload
            )
        )

        return booking


import asyncio
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Payment, Booking, Notification
from notification_router import NotificationWebSocketManager


class PaymentRepository:

    @staticmethod
    async def initialize_payment(
        db: AsyncSession,
        booking_id: int,
        amount: Decimal,
        method: str
    ) -> Payment:

        payment = Payment(
            booking_id=booking_id,
            amount=amount,
            method=method,
            status="Pending"
        )

        db.add(payment)
        await db.commit()
        await db.refresh(payment)

        return payment

    @staticmethod
    async def complete_payment(
        db: AsyncSession,
        payment_id: int,
        transaction_id: str
    ) -> Payment | None:

        try:
            # Find payment
            result = await db.execute(
                select(Payment).where(Payment.payment_id == payment_id)
            )
            payment = result.scalar_one_or_none()

            if not payment:
                return None

            # Prevent duplicate payment
            if payment.status == "Completed":
                return payment

            # Find booking
            booking_result = await db.execute(
                select(Booking).where(Booking.id == payment.booking_id)
            )
            booking = booking_result.scalar_one_or_none()

            if not booking:
                return None

            # Update payment
            payment.status = "Completed"
            payment.transaction_id = transaction_id

            # Update booking
            booking.status = "Confirmed"

            # Customer notification
            customer_notification = Notification(
                user_id=booking.customer_id,
                message=f"Payment Successful! Your booking for '{booking.job_title}' is now Confirmed. (Booking ID: #{booking.id})",
                type="Payment_Success"
            )

            # Provider notification
            provider_notification = Notification(
                user_id=booking.provider_id,
                message=f"Payment Received! Customer has paid for the booking '{booking.job_title}'. (Booking ID: #{booking.id})",
                type="Payment_Received"
            )

            db.add(customer_notification)
            db.add(provider_notification)

            # Generate notification IDs
            await db.flush()

            customer_ws_message = {
                "notification_id": customer_notification.notification_id,
                "message": customer_notification.message,
                "type": customer_notification.type,
                "is_read": False
            }

            provider_ws_message = {
                "notification_id": provider_notification.notification_id,
                "message": provider_notification.message,
                "type": provider_notification.type,
                "is_read": False
            }

            # Save everything
            await db.commit()

            # Refresh payment
            await db.refresh(payment)

            # Send WebSocket notifications
            asyncio.create_task(
                NotificationWebSocketManager.send_personal_notification(
                    user_id=booking.customer_id,
                    message=customer_ws_message
                )
            )

            asyncio.create_task(
                NotificationWebSocketManager.send_personal_notification(
                    user_id=booking.provider_id,
                    message=provider_ws_message
                )
            )

            return payment

        except Exception:
            await db.rollback()
            raise
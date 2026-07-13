from fastapi import HTTPException
from langchain_classic.chains.question_answering.map_reduce_prompt import messages
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db_models import Notification
from resp_models import NotificationCreate


class NotificationRepository:
    @staticmethod
    async def create_notification(db:AsyncSession, notif_data: NotificationCreate):
        db_notif = Notification(
            user_id=notif_data.user_id,
            messages=notif_data.message,
            type=notif_data.type
        )
        db.add(db_notif)
        await db.commit()
        await db.refresh(db_notif)
        return db_notif

    @staticmethod
    async def get_user_notifications(db:AsyncSession, user_id:int):
        query = await db.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )

        return query.scalars().all()

    @staticmethod
    async def mark_as_read(db:AsyncSession, notification_id:int):
        query = await db.execute(
            select(Notification).where(Notification.notification_id == notification_id)
        )
        notif = query.scalars().first()
        if not notif:
            raise HTTPException(
                status_code=404,
                detail="Notifications not found."
            )
        notif.is_read = True
        await db.commit()
        await db.refresh(notif)
        return notif

    @staticmethod
    async def get_unread_notifications(db:AsyncSession, user_id:int):
        result = await db.execute(
            select(func.count(Notification.notification_id))
            .where(Notification.user_id == user_id, Notification.is_read == False)
        )
        return result.scalar_one_or_none() or 0

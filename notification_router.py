from typing import List, Dict

from fastapi import APIRouter,status,Depends,WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect

from database_config import get_db
from notification_ropository import NotificationRepository
from resp_models import NotificationCreate, NotificationResponse

router = APIRouter()
notif_repo = NotificationRepository()

class NotificationWebSocketManager:
    active_connections: Dict[int, WebSocket] = {}

    @staticmethod
    async def connect(user_id: int, websocket:WebSocket):
        await websocket.accept()
        NotificationWebSocketManager.active_connections[user_id] = websocket

    @staticmethod
    async def disconnect(user_id:int ):
        if user_id in NotificationWebSocketManager.active_connections[user_id]:
            del NotificationWebSocketManager.active_connections[user_id]

    @staticmethod
    async def send_personal_notification(user_id:int, message:dict):
        if user_id in NotificationWebSocketManager.active_connections:
            websocket = NotificationWebSocketManager.active_connections[user_id]
            await websocket.send_json(message)

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket:WebSocket, user_id:int):
    await  NotificationWebSocketManager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await NotificationWebSocketManager.disconnect(user_id)


@router.get("/user/{user_id}",response_model=List[NotificationResponse])
async def  read_user_notifications(user_id: int, db:AsyncSession = Depends(get_db)):
    return await notif_repo.get_user_notifications(db,user_id)

@router.patch("/{notification_id}/read",response_model=NotificationResponse)
async def mark_notifications_as_read(notification_id:int, db:AsyncSession = Depends(get_db)):
    return await notif_repo.mark_as_read(db, notification_id)

@router.get("/user/{user_id}/unread-count",status_code=status.HTTP_200_OK)
async def get_user_unread_notification_count(user_id: int, db:AsyncSession = Depends(get_db)):
    count = await NotificationRepository.get_unread_notifications(db,user_id)
    return {"user_id": user_id, "unread_count": count}

from sqlmodel.ext.asyncio.session import AsyncSession
from app.notifications.models import Notification 
from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import select, update
import uuid as uuid_pkg
from typing import List

class NotificationsCRUD:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: dict):
        pass

    async def get(self, uuid: uuid_pkg.UUID) -> Notification:
        query = select(Notification).where(Notification.uuid == uuid)
        results = await self.session.execute(query)
        notification = results.scalar_one_or_none()
        if notification is None:
            raise HTTPException(http_status.HTTP_404_NOT_FOUND,
                                detail="Notification with such uuid not found")
        return notification
    
    async def get_all_user(self, user_uuid: uuid_pkg.UUID) -> List[Notification]:
        query = select(Notification.uuid, Notification.data, Notification.type, Notification.created_at, 
                    Notification.updated_at, Notification.toUser, Notification.viewed).where(Notification.toUser == user_uuid)
        data = await self.session.execute(query)
        return data.fetchall()
    
    async def get_active_notifications(self, user_uuid: uuid_pkg.UUID):
        query = select(Notification.uuid, Notification.data, Notification.type, Notification.created_at, 
                    Notification.updated_at, Notification.toUser, Notification.viewed).where(Notification.toUser == user_uuid, Notification.viewed == False)
        data = await self.session.execute(query)
        return data.fetchall()

    async def set_readed(self, uuid: uuid_pkg.UUID):
        query = update()
    
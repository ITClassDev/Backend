from sqlmodel.ext.asyncio.session import AsyncSession
from app.notifications.models import Notification
from app.notifications.schemas import NotificationCreate
from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import select, update
import uuid as uuid_pkg
from typing import List

class NotificationsCRUD:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_single(self, notification: NotificationCreate) -> Notification:
        values = notification.dict()
        values.pop("toGroup")
        notification = Notification(**values)
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification


    async def create(self, notification: NotificationCreate) -> None:
        toUser = notification.toUser
        toGroup = notification.toGroup
        if toUser:
            return await self.create_single(notification)
        elif toGroup:
            pass
        else:
            raise HTTPException(http_status.HTTP_400_BAD_REQUEST, 
                                detail="toUser and toGroup can't both be defined in request. Only one have to be defined.")

    async def get(self, uuid: uuid_pkg.UUID) -> Notification:
        query = select(Notification).where(Notification.uuid == uuid)
        results = await self.session.execute(query)
        notification = results.scalar_one_or_none()
        if notification is None:
            raise HTTPException(http_status.HTTP_404_NOT_FOUND,
                                detail="Notification with such uuid not found")
        return notification
    
    async def get_all_user(self, user_uuid: uuid_pkg.UUID) -> List[Notification]:
        query = select(Notification).where(Notification.toUser == user_uuid)
        data = await self.session.execute(query)
        return data.fetchall()
    
    async def get_active_notifications(self, user_uuid: uuid_pkg.UUID) -> List[Notification]:
        query = select(Notification.uuid, Notification.data, Notification.type, Notification.created_at, 
                    Notification.updated_at, Notification.toUser, Notification.viewed).where(Notification.toUser == user_uuid, Notification.viewed == False)
        data = await self.session.execute(query)
        return data.fetchall()

    async def set_readed(self, uuid: uuid_pkg.UUID):
        query = update()
    
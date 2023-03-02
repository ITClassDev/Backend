from db.notifications import notifications
from .base import BaseRepository
from models.notifications import Notification
from typing import List
import json
from sqlalchemy import insert


class NotificationRepository(BaseRepository):
    async def get_all_for_user(self, user_id: int) -> List[Notification]:
        await self.set_viewed(user_id)
        query = notifications.select().where(notifications.c.to_user == user_id).order_by(notifications.c.id.desc())
        return await self.database.fetch_all(query)

    async def check_active_notifications(self, user_id: int) -> bool:
        query = notifications.select().where(notifications.c.to_user == user_id, notifications.c.viewed == False)
        return len(await self.database.fetch_all(query)) > 0

    async def send_notification(self, user_id: int, notification_type: int, data: dict) -> int:
        notification = Notification(to_user=user_id, type=notification_type, viewed=False, data=data)
        values = {**notification.dict()}
        values.pop("id", None)
        query = notifications.insert().values(**values)
        return await self.database.execute(query)

    async def set_viewed(self, user_id: int) -> None:
        query = notifications.update().where(notifications.c.to_user == user_id, notifications.c.viewed != True).values(viewed=True)
        await self.database.execute(query)
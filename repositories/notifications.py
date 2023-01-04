from db.notifications import notifications
from .base import BaseRepository
from models.notifications import Notification
from typing import List


class NotificationRepository(BaseRepository):
    async def get_all_for_user(self, user_id: int) -> List[Notification]:
        query = notifications.select().where(notifications.c.to_user == user_id).order_by(notifications.c.id.desc())
        return await self.database.fetch_all(query)

    async def check_active_notifications(self, user_id: int) -> bool:
        query = notifications.select().where(notifications.c.to_user == user_id, notifications.c.viewed == False)
        return len(await self.database.fetch_all(query)) > 0
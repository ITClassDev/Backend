from db.notifications import notifications
from .base import BaseRepository
from models.notifications import Notification
from typing import List


class NotificationRepository(BaseRepository):
    async def get_all_for_user(self, user_id: int) -> List[Notification]:
        query = notifications.select().where(notifications.c.to_user == user_id)
        res = await self.database.fetch_all(query)
        return res
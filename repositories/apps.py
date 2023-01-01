from db.apps import apps
from .base import BaseRepository
from models.apps import App
from typing import List


class AppsRepository(BaseRepository):
    async def get_by_id(self, id: int) -> App:
        query = apps.select().where(apps.c.id == id)
        return await self.database.fetch_one(query)

    async def get_for_user(self, user_id: int) -> List[App]:
        query = apps.select().where(apps.c.owner_id == user_id)
        return await self.database.fetch_all(query)
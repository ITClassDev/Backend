from db.apps import apps
from .base import BaseRepository
from models.apps import App


class AppsRepository(BaseRepository):
    async def get_by_id(self, id: int) -> App:
        query = apps.select().where(apps.c.id == id)
        return await self.database.fetch_one(query)
from db.apps import apps
from .base import BaseRepository
from models.apps import App, AppIn
from typing import List
import datetime


class AppsRepository(BaseRepository):
    async def get_by_id(self, id: int) -> App:
        query = apps.select().where(apps.c.id == id)
        return await self.database.fetch_one(query)

    async def get_for_user(self, user_id: int) -> List[App]:
        query = apps.select().where(apps.c.owner_id == user_id)
        return await self.database.fetch_all(query)

    async def create_app(self, app_data: AppIn, owner_id: int) -> int:
        app_obj = App(name=app_data.name, redirect_url=app_data.redirect_url, owner_id=owner_id, permission_level=1, verified=1, created_at=datetime.datetime.now())
        print(app_obj)
        values = {**app_obj.dict()}
        values.pop("id", None)
        query = apps.insert().values(**values)
        app_id = await self.database.execute(query)
        return app_id
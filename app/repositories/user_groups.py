from db.user_groups import user_groups
from models.user_groups import UserGroup
from .base import BaseRepository
from typing import List

class UserGroupsRepository(BaseRepository):
    async def get_all(self) -> List[UserGroup]:
        query = user_groups.select()
        return await self.database.fetch_all(query)

    async def create(self, name: str) -> int:
        values = {**UserGroup(name=name).dict()}
        values.pop("id", None)
        query = user_groups.insert().values(**values)
        return await self.database.execute(query)

    async def delete(self, id: int) -> None:
        query = user_groups.delete().where(user_groups.c.id == id)
        return await self.database.execute(query)

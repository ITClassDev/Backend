from db.user_groups import user_groups
from models.user_groups import UserGroup
from .base import BaseRepository
from typing import List

class UserGroupsRepository(BaseRepository):
    async def get_all(self) -> List[UserGroup]:
        query = user_groups.select()
        return await self.database.fetch_all(query)

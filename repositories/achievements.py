from db.achievements import achievements
from typing import List
from .base import BaseRepository
from models.achievements import Achievement

class AchievementRepository(BaseRepository):
    async def get_by_id():
        pass   

    async def get_all_for_user(self, user_id: int) -> List[Achievement]:
        query = achievements.select().where(achievements.c.to_user == user_id)
        result_data = await self.database.fetch_all(query)
        return result_data

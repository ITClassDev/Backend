from db.achievements import achievements
from typing import List
from .base import BaseRepository
from models.achievements import Achievement, AchievementIn
import datetime

class AchievementRepository(BaseRepository):
    async def get_by_id():
        pass   

    async def get_all_for_user(self, user_id: int) -> List[Achievement]:
        query = achievements.select().where(achievements.c.to_user == user_id, achievements.c.accepted_by != None)
        result_data = await self.database.fetch_all(query)
        return result_data

    async def add(self, achievement: AchievementIn, to_user_id: int) -> Achievement:
        achievement_final = Achievement(
            to_user=to_user_id,
            type=achievement.type,
            title=achievement.title,
            description=achievement.description,
            points=0,
            received_at=datetime.datetime.now()
        )
        values = {**achievement_final.dict()}
        values.pop("id", None)
        values.pop("accepted_by", None)
        query = achievements.insert().values(**values)
        result = await self.database.execute(query)
        print(result)
        return result
    
    async def change_status(self, achievement_id: int, accepted_by, accept=True):
        pass
    async def get_moderation_queue_for_one(self, for_user_id: int):
        pass
    async def get_moderation_queue_for_all(self):
        pass

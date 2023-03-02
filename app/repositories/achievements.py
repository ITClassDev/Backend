from db.achievements import achievements
from db.users import users
from typing import List
from .base import BaseRepository
from models.achievements import Achievement, AchievementIn
import datetime
from fastapi import Depends
from db.base import database
from .notifications import NotificationRepository


class AchievementRepository(BaseRepository):
    async def get_by_id():
        pass   

    async def get_category_for_user(self, user_id: int, achievement_type: int = 0) -> List[Achievement]:
        # Type 0: Olimpiads
        # Type 1: events
        # Type 2: system
        query = achievements.select().where(achievements.c.to_user == user_id, achievements.c.accepted_by != None, achievements.c.type == achievement_type)
        data = await self.database.fetch_all(query)
        return data

    async def get_all_for_user(self, user_id: int) -> List[Achievement]:
        query = achievements.select().where(achievements.c.to_user == user_id, achievements.c.accepted_by != None)
        data = await self.database.fetch_all(query)
        return data


    async def add(self, achievement: AchievementIn, to_user_id: int, uploaded_image: dict) -> Achievement:
        achievement_final = Achievement(
            to_user=to_user_id,
            type=achievement.type,
            title=achievement.title,
            description=achievement.description,
            points=0,
            received_at=datetime.datetime.now(),
            attachment_file_name=uploaded_image["file_name"]
        )
        values = {**achievement_final.dict()}
        values.pop("id", None)
        values.pop("accepted_by", None)
        query = achievements.insert().values(**values)
        achievement_final = await self.database.execute(query)
        return achievement_final
    
    async def accept(self, achievement_id: int, accepted_by: int, points: int):
        notifications = NotificationRepository(database)
        # TODO
        # Check if achievement already accepted by another moderator
        query = achievements.select().where(achievements.c.id == achievement_id)
        achievement_data = await self.database.fetch_one(query)
        to_user_id = achievement_data.to_user
        # Send notification to user
        await notifications.send_notification(to_user_id, 0, {"name": achievement_data.title, "points": points})

        # Add points to user rating
        query = users.update().where(users.c.id == to_user_id).values({"rating": users.c.rating + points})
        await self.database.execute(query)

        # Accept achievement
        query = achievements.update().where(achievements.c.id == achievement_id).values({"accepted_by": accepted_by, "points": points})
        await self.database.execute(query)

    async def delete(self, achievement_id):
        notifications = NotificationRepository(database)
        query = achievements.select().where(achievements.c.id == achievement_id)
        achievement_data = await self.database.fetch_one(query)
        to_user_id = achievement_data.to_user
        # Send notification to user
        await notifications.send_notification(to_user_id, 1, {"name": achievement_data.title})

        query = achievements.delete().where(achievements.c.id == achievement_id)
        return await self.database.execute(query)

    async def get_moderation_queue_for_one(self, for_user_id: int) -> List[Achievement]:
        query = achievements.select().where(achievements.c.to_user == for_user_id, achievements.c.accepted_by == None)
        return await self.database.fetch_all(query)
    async def get_moderation_queue_for_all(self) -> List[Achievement]:
        query = achievements.select().where(achievements.c.accepted_by == None)
        return await self.database.fetch_all(query)
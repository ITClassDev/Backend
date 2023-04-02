from db.polls import polls, polls_answers
from models.polls import Poll, PollIn, PollAnswer
from .base import BaseRepository
import random
from typing import List
import datetime


class PollsRepository(BaseRepository):
    async def get_all(self, offset: int, limit: int) -> List[Poll]:
        return await self.database.fetch_all(polls.select().offset(offset).limit(limit).order_by(polls.c.created_at.desc()))

    async def get_by_id(self, id: int) -> Poll:
        return await self.database.fetch_one(polls.select().where(polls.c.id == id))

    async def create_poll(self, poll_data: PollIn, owner_id: int) -> int:
        poll_obj = Poll(**poll_data.dict(), owner_id=owner_id,
                        created_at=datetime.datetime.now(), id=random.randint(10 ** 4, 10 ** 6))
        values = {**poll_obj.dict()}
        query = polls.insert().values(**values)
        await self.database.execute(query)
        return values["id"]

    async def submit_answers(self, id: int, answers: dict, user_id: int = None) -> int:
        poll_answers_obj = PollAnswer(poll_id=id, user_id=user_id, answers=answers)
        values = {**poll_answers_obj.dict()}
        values.pop("id", None)
        query = polls_answers.insert().values(**values)
        return await self.database.execute(query)
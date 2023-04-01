from db.polls import polls
from models.polls import Poll, PollIn
from .base import BaseRepository
import random
from typing import List
import datetime


class PollsRepository(BaseRepository):
    async def get_by_id(self, poll_id: int) -> Poll:
        pass

    async def create_poll(self, poll_data: PollIn, owner_id: int) -> int:
        poll_obj = Poll(**poll_data.dict(), owner_id=owner_id, created_at=datetime.datetime.now(), id=random.randint(10 ** 4, 10 ** 6))
        values = {**poll_obj.dict()}
        query = polls.insert().values(**values)
        poll_id = await self.database.execute(query)
        return poll_id
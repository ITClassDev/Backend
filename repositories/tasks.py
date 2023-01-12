from db.tasks import tasks
from .base import BaseRepository
from models.tasks import Task, TaskIn
from sqlalchemy import select

class TasksRepository(BaseRepository):
    async def get_by_id(self, task_id: int) -> Task:
        query = select(tasks.c.id, tasks.c.author_id, tasks.c.title, tasks.c.text, tasks.c.time_limit, tasks.c.memory_limit, tasks.c.is_day_challenge).where(tasks.c.id == task_id)
        return await self.database.fetch_one(query)

    async def add(self, task_data: TaskIn, author_id: int) -> int:
        task_obj = Task(**dict(task_data), author_id=author_id)
        values = {**task_obj.dict()}
        values.pop("id", None)
        query = tasks.insert().values(**values)
        task_id = await self.database.execute(query)
        return task_id


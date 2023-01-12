from db.tasks import tasks
from db.submits import submits
from .base import BaseRepository
from models.tasks import Task, TaskIn
from models.submits import Submit
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
    
    async def get_day_challenge(self) -> dict:
        query = tasks.select().where(tasks.c.is_day_challenge == True)
        return await self.database.fetch_one(query)

    async def submit_day_challenge(self, user_id: int, source_path: str) -> Submit:
        task_id = self.get_day_challenge()
        submit = Submit(user_id=user_id, status=0, task_id=task_id, source=f"file:{source_path}", refer_to=None, git_commit_id=None, solved=False, tests_results=[])
        values = {**submit.dict()}
        query = submits.insert().values(**values)
        return await self.database.execute(query)
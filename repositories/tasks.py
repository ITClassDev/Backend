from db.tasks import tasks
from db.submits import submits
from .base import BaseRepository
from models.tasks import Task, TaskIn
from models.submits import Submit
from sqlalchemy import select
from typing import List
import os
import pickle
from core.config import USERS_STORAGE



class TasksRepository(BaseRepository):
    async def get_by_id(self, task_id: int) -> Task:
        query = select(tasks.c.id, tasks.c.author_id, tasks.c.title, tasks.c.text, tasks.c.time_limit, tasks.c.memory_limit, tasks.c.is_day_challenge).where(tasks.c.id == task_id)
        return await self.database.fetch_one(query)

    async def add(self, task_data: TaskIn, author_id: int) -> int:
        if task_data.is_day_challenge:
            query = tasks.update().values(is_day_challenge=False)
            await self.database.execute(query)
        task_obj = Task(**dict(task_data), author_id=author_id)
        values = {**task_obj.dict()}
        values.pop("id", None)
        query = tasks.insert().values(**values)
        task_id = await self.database.execute(query)
        return task_id
    
    async def get_day_challenge(self) -> dict:
        query = tasks.select().where(tasks.c.is_day_challenge == True)
        return await self.database.fetch_one(query)

    async def checker_callback(self, data):
        solved, tests_results_log, task_id = data
        #query = submits.update().
        

    async def submit_day_challenge(self, user_id: int, source_path: str, checker) -> Submit:
        task_id = await self.get_day_challenge()
        task_data = await self.database.fetch_one(tasks.select().where(tasks.c.id == task_id.id)) # Get task data
        tests = pickle.loads(task_data.tests)

        with open(os.path.join(USERS_STORAGE, "tasks_source_codes", source_path["file_name"]), "rb") as source_file:
            source = source_file.read()
            print(source)
            checker.check_one_task(source, tests, lambda res: print(res), int(task_id.id))
        submit = Submit(user_id=user_id, status=0, task_id=task_id.id, source=f"file:{source_path['file_name']}", refer_to=None, git_commit_id=None, solved=False, tests_results=[])
        values = {**submit.dict()}
        values.pop("id", None)
        query = submits.insert().values(**values)
        submit_id = await self.database.execute(query)
        return submit_id

    async def get_task_submits(self, user_id: int, task_id: int) -> List[Submit]:
        query = submits.select().where(submits.c.user_id == user_id, submits.c.task_id == task_id).order_by(submits.c.id.desc())
        return await self.database.fetch_all(query)

    async def get_day_challenge_submits(self, user_id: int):
        day_challenge = await self.get_day_challenge()
        return await self.get_task_submits(user_id, day_challenge.id)

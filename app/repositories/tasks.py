from db.tasks import tasks
from db.submits import submits
from db.contests import contests
from .base import BaseRepository
from models.tasks import Task, TaskIn
from models.submits import Submit
from models.contests import Contest, ContestIn
from sqlalchemy import select
from typing import List
import os
import pickle
from core.config import USERS_STORAGE
import asyncio
import threading
import datetime


class TasksRepository(BaseRepository):
    async def get_by_id(self, task_id: int) -> Task:
        query = select(tasks.c.id, tasks.c.author_id, tasks.c.title, tasks.c.text, tasks.c.time_limit, tasks.c.memory_limit, tasks.c.is_day_challenge).where(tasks.c.id == task_id)
        return await self.database.fetch_one(query)

    async def get_by_id_full(self, task_id: int) -> Task:
        query = tasks.select().where(tasks.c.id == task_id)
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

    async def get_all(self, limit: int = 20) -> List[Task]:
        query = select(tasks.c.id, tasks.c.author_id, tasks.c.title, tasks.c.text, tasks.c.time_limit, tasks.c.memory_limit, tasks.c.is_day_challenge).limit(limit).order_by(tasks.c.id.desc())
        return await self.database.fetch_all(query)
    
    async def get_day_challenge(self) -> dict:
        query = tasks.select().where(tasks.c.is_day_challenge == True)
        return await self.database.fetch_one(query)

    def checker_callback(self, data, loop):
        solved, tests_results_log, submit_id = data
        query = submits.update().where(submits.c.id == submit_id).values(status=2, solved=solved, tests_results=tests_results_log)
        loop.create_task(self.database.execute(query))

    def checker_homework_callback(self, data, loop):
        for submission in data:
            query = submits.update().where(submits.c.id == submission).values(status=2, solved=data[submission][0], tests_results=data[submission][1])
            loop.create_task(self.database.execute(query))

    async def submit_day_challenge(self, user_id: int, source_path: str, checker) -> Submit:
        # Create submit
        task_id = await self.get_day_challenge()
        submit = Submit(user_id=user_id, status=0, task_id=task_id.id, source=f"file:{source_path['file_name']}", refer_to=None, git_commit_id=None, solved=False, tests_results=[], send_date=datetime.datetime.now())
        values = {**submit.dict()}
        values.pop("id", None)
        query = submits.insert().values(**values)
        submit_id = await self.database.execute(query)
        task_data = await self.database.fetch_one(tasks.select().where(tasks.c.id == task_id.id)) # Get task data
        tests = pickle.loads(task_data.tests)
        env = {"cpu_time_limit": task_data.time_limit, "memory_limit": task_data.memory_limit, "real_time_limit": task_data.time_limit}
        # Start checker process; async loop
        with open(os.path.join(USERS_STORAGE, "tasks_source_codes", source_path["file_name"]), "rb") as source_file:
            source = source_file.read()
            loop = asyncio.get_event_loop()
            thread = threading.Thread(target=lambda: checker.check_one_task_thread(source, source_path["file_name"], tests, env, self.checker_callback, submit_id, loop))
            thread.start()
            
        return submit_id

    async def get_task_submits(self, user_id: int, task_id: int) -> List[Submit]:
        query = submits.select().where(submits.c.user_id == user_id, submits.c.task_id == task_id).order_by(submits.c.id.desc())
        return await self.database.fetch_all(query)

    async def get_day_challenge_submits(self, user_id: int):
        day_challenge = await self.get_day_challenge()
        return await self.get_task_submits(user_id, day_challenge.id)

    async def create_contest(self, contest_data: ContestIn, user_id: int):
        contest_obj = Contest(author_id = user_id, **dict(contest_data))
        values = {**dict(contest_obj)}
        values.pop("id", None)
        query = contests.insert().values(**values)

        contest_id = await self.database.execute(query)
        return contest_id

    async def get_contest_tasks(self, contest_id: int):
        query = contests.select().where(contests.c.id == contest_id)
        contest_tasks = await self.database.fetch_one(query)
        #contest_tasks = contest_tasks.tasks_ids_list
        return contest_tasks

    async def get_contest_task_submits(self, task_id, contest_id):
        query = submits.select().where(submits.c.task_id == task_id, submits.c.refer_to == contest_id).order_by(submits.c.id.desc())
        return await self.database.fetch_all(query)


    async def submit_contest(self, contest_id: int, git_url: str, user_id: int, language: str, checker):
        tasks_all = await self.get_contest_tasks(contest_id)
        checker_payload = []
        for task in tasks_all.tasks_ids_list:
            task_data = await self.get_by_id_full(task)
            tests = pickle.loads(task_data.tests)
            types = task_data.input_types
            func_name = task_data.func_name
            submit = Submit(user_id=user_id, status=0, task_id=task, source=f"git:{git_url}", refer_to=contest_id, git_commit_id="testst", solved=False, tests_results=[], send_date=datetime.datetime.now())
            values = {**submit.dict()}
            values.pop("id", None)
            query = submits.insert().values(**values)
            submit_id = await self.database.execute(query)
            env = {"cpu_time_limit": task_data.time_limit, "memory_limit": task_data.memory_limit, "real_time_limit": task_data.time_limit}
            checker_payload.append({func_name: {"tests": tests, "submit_id": submit_id, "types": types, "env": env}})
        loop = asyncio.get_event_loop()
        thread = threading.Thread(target=lambda: checker.check_multiple_tasks(git_url, checker_payload, lambda data, loop: self.checker_homework_callback(data, loop), loop))
        thread.start()

            

    async def get_submission_details(self, submission_id: int):
        submission = submits.select().where(submits.c.id == submission_id)
        return await self.database.fetch_one(submission)
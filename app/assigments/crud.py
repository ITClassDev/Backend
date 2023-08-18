from sqlmodel.ext.asyncio.session import AsyncSession
import sqlalchemy
from sqlalchemy import select, update
from fastapi import HTTPException
from fastapi import status as http_status
import uuid as uuid_pkg
from app.assigments.models import Task, Contest, Submit
from app.assigments.schemas import TaskCreate
from typing import List, Tuple

class TasksCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: TaskCreate, author_id: uuid_pkg.UUID) -> Task:
        values = task.dict()
        values["authorId"] = author_id
        try:
            task = Task(**values)
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)
            return task
        except sqlalchemy.exc.IntegrityError as e:  # type: ignore
            err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
            raise HTTPException(
                http_status.HTTP_400_BAD_REQUEST, detail=err_msg)
        
    def only_example_tests(self, task: Task) -> Task:
        task.tests = list(filter(lambda test: 'example' in test and test['example'], task.tests))
        return task
        
    async def get(self, task_uuid: uuid_pkg.UUID) -> Task | None:
        query = select(Task).where(Task.uuid == task_uuid)
        results = await self.session.execute(query)
        task = results.scalar_one_or_none()
        if not task:
            raise HTTPException(
                http_status.HTTP_404_NOT_FOUND, detail="Task with such uuid not found")
        
        return task
        
    async def get_day_challenge(self) -> Task | None:
        query = select(Task).where(Task.dayChallenge == True)
        results = await self.session.execute(query)
        task = results.scalar_one_or_none()
        if not task:
            raise HTTPException(
                http_status.HTTP_404_NOT_FOUND, detail="No day challenge for now")
        return self.only_example_tests(task)
        
    async def get_all(self) -> List[Task]:
        results = await self.session.execute(select(Task))
        return [tuple(row)[0] for row in results]
    
    async def search(self, query: str) -> List[Task]:
        results = await self.session.execute(select(Task.uuid, Task.title).filter(Task.title.like(f'%{query}%')))
        return results.fetchall()
    
    async def set_challenge(self, uuid: uuid_pkg.UUID) -> Task:
        query_0 = update(Task).where(Task.uuid == uuid).values(dayChallenge=True) # Set task as day challenge
        query_1 = update(Task).where(Task.uuid != uuid).values(dayChallenge=False) # Set other as not day challenge
        await self.session.execute(query_0)
        await self.session.execute(query_1)
        await self.session.commit()
        day_challenge = select(Task).where(Task.dayChallenge == True)
        day_challenge = await self.session.execute(day_challenge)
        return day_challenge.fetchall()


class ContestsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

class SubmitsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.tasks_crud = TasksCRUD(self.session)

    async def get_users_for_tasks(self, task_uuid: uuid_pkg.UUID, user_uuid: uuid_pkg.UUID):
        query = select(Submit).where(Submit.userId == user_uuid, Submit.taskId == task_uuid)
        results = await self.session.execute(query)
        return results.fetchall()
    
    async def submit(self, source: str, user_uuid: uuid_pkg.UUID, task_uuid: uuid_pkg.UUID = None, task_object: Task = None) -> Submit:
        '''
        Task uuid based used in contest's endpoints
        Direct task object used in day challenge, to prevent day challenge reselect
        '''
        # Resolve task obj
        # Statuses: 0 - Pending; 1 - Checking; 2 - Checked
        task = task_object
        if not task: task = await self.tasks_crud.get(task_uuid)
        task_uuid = task.uuid
        submit = Submit(status=1, taskId=task_uuid, source=source, solved=False, userId=user_uuid)
        self.session.add(submit)
        await self.session.commit()
        await self.session.refresh(submit)
        return submit

    async def get(self, uuid: uuid_pkg.UUID, user_id: uuid_pkg.UUID) -> Submit:
        query = select(Submit).where(Submit.uuid == uuid and Submit.userId == user_id)
        results = await self.session.execute(query)
        if results:
            return results.scalar_one_or_none()
        raise HTTPException(
            http_status.HTTP_404_NOT_FOUND, detail="No such submit"
        )
    
    async def submit_day_challenge(self, source: str, user_uuid: uuid_pkg.UUID) -> Submit:
        day_challenge = await self.tasks_crud.get_day_challenge()
        if day_challenge:
            return await self.submit(source, user_uuid, task_object=day_challenge)
            
        raise HTTPException(
            http_status.HTTP_400_BAD_REQUEST, detail="No day challenge for now")
    
    async def day_challenge_user_submits(self, user_uuid: uuid_pkg.UUID) -> List[Submit]:
        day_challenge = await self.tasks_crud.get_day_challenge()
        if day_challenge:
            query = select(Submit).where(Submit.userId == user_uuid, Submit.taskId == day_challenge.uuid, Submit.referedContest.is_(None)).order_by(Submit.created_at.desc())
            results = await self.session.execute(query)
            return [tuple(row)[0] for row in results.fetchall()]
            
        raise HTTPException(
            http_status.HTTP_400_BAD_REQUEST, detail="No day challenge for now")
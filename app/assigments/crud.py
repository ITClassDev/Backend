from sqlmodel.ext.asyncio.session import AsyncSession
import sqlalchemy
from sqlalchemy import select
from fastapi import HTTPException
from fastapi import status as http_status
import uuid as uuid_pkg
from app.assigments.models import Task, Contest, Submit
from app.assigments.schemas import TaskCreate
from typing import List

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
        
    async def get(self, task_uuid: uuid_pkg.UUID) -> Task | None:
        query = select(Task).where(Task.uuid == task_uuid)
        results = await self.session.execute(query)
        task = results.scalar_one_or_none()
        if not task:
            raise HTTPException(
                http_status.HTTP_404_NOT_FOUND, detail="Task with such uuid not found")
        else:
            return task
        
    async def get_all(self) -> List[Task]:
        results = await self.session.execute(select(Task))
        return [tuple(row)[0] for row in results]


        

class ContestsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

class SubmitsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
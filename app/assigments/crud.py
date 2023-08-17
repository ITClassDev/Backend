from sqlmodel.ext.asyncio.session import AsyncSession
from app.assigments.models import Task, Contest, Submit
from app.assigments.schemas import TaskCreate

class TasksCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(task: TaskCreate) -> Task:
        pass

class ContestsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

class SubmitsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
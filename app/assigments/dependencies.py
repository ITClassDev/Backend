from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.assigments.crud import TasksCRUD, ContestsCRUD, SubmitsCRUD


async def get_tasks_crud(
        session: AsyncSession = Depends(get_async_session)
) -> TasksCRUD:
    return TasksCRUD(session=session)

async def get_contests_crud(
        session: AsyncSession = Depends(get_async_session)
) -> ContestsCRUD:
    return ContestsCRUD(session=session)

async def get_submits_crud(
        session: AsyncSession = Depends(get_async_session)
) -> SubmitsCRUD:
    return SubmitsCRUD(session=session)
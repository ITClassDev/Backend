from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.groups.crud import GroupsCRUD


async def get_groups_crud(
        session: AsyncSession = Depends(get_async_session)
) -> GroupsCRUD:
    return GroupsCRUD(session=session)
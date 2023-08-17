from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.users.crud import UsersCRUD


async def get_users_crud(
        session: AsyncSession = Depends(get_async_session)
) -> UsersCRUD:
    return UsersCRUD(session=session)
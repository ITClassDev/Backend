from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.achievements.crud import AchievementsCRUD


async def get_achievements_crud(
        session: AsyncSession = Depends(get_async_session)
) -> AchievementsCRUD:
    return AchievementsCRUD(session=session)
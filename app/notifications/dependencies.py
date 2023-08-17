from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.notifications.crud import NotificationsCRUD


async def get_notifications_crud(
        session: AsyncSession = Depends(get_async_session)
) -> NotificationsCRUD:
    return NotificationsCRUD(session=session)
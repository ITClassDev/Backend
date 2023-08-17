from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from fastapi import status as http_status
import uuid as uuid_pkg
from sqlalchemy import select
from typing import List
from app.achievements.models import Achievement
from app.achievements.schemas import AchievementCreate
from app.users.models import User
import uuid as uuid_pkg


class AchievementsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: AchievementCreate, user_uuid: uuid_pkg.UUID, attachmentName: str) -> Achievement:
        values = data.dict()
        values["toUser"] = user_uuid
        values["attachmentName"] = attachmentName
        try:
            achievement = Achievement(**values)
            self.session.add(achievement)
            await self.session.commit()
            await self.session.refresh(achievement)
            return achievement
        except sqlalchemy.exc.IntegrityError as e:  # type: ignore
            err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
            raise HTTPException(
                http_status.HTTP_400_BAD_REQUEST, detail=err_msg)

    async def update():
        pass

    # async def get(self, uuid: uuid_pkg.UUID) -> Group:
    #     query = select(Group).where(Group.uuid == uuid)
    #     results = await self.session.execute(query)
    #     user = results.scalar_one_or_none()
    #     if user is None:
    #         raise HTTPException(http_status.HTTP_404_NOT_FOUND,
    #                             detail="Group with such uuid not found")
    #     return user


    async def get_all_for_user(self, user_uuid: uuid_pkg.UUID, active: bool = True) -> List[Achievement]:
        columns = (Achievement.uuid, Achievement.eventType, Achievement.attachmentName, Achievement.points, Achievement.acceptedAt, Achievement.acceptedBy, Achievement.acceptedAt, Achievement.title, Achievement.description, Achievement.created_at, User)
        if active: # Moderated OK
            query = select(*columns).where(Achievement.toUser == user_uuid, User.uuid == user_uuid, Achievement.acceptedBy != None, Achievement.acceptedAt != None)
        else: # In moderation queue
            query = select(*columns).where(Achievement.toUser == user_uuid, User.uuid == user_uuid, Achievement.acceptedBy == None, Achievement.acceptedAt == None)
        results = await self.session.execute(query.order_by(Achievement.created_at.desc()))
        return results.fetchall()
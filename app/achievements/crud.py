from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from fastapi import status as http_status
import uuid as uuid_pkg
import sqlalchemy
from sqlalchemy import select, update, delete
from typing import List
from app.achievements.models import Achievement
from app.achievements.schemas import AchievementCreate, AchievementModerate
from app.notifications.schemas import NotificationCreate
from app.notifications.crud import NotificationsCRUD
from app.users.models import User
import uuid as uuid_pkg
import datetime


class AchievementsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.columns = (Achievement.uuid, Achievement.eventType, Achievement.attachmentName, Achievement.points, Achievement.acceptedAt, Achievement.acceptedBy, Achievement.acceptedAt, Achievement.title, Achievement.description, Achievement.created_at, User)

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
            print(e)
            err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
            raise HTTPException(
                http_status.HTTP_400_BAD_REQUEST, detail=err_msg)

    async def all_queue(self):
        query = select(*self.columns).where(User.uuid == Achievement.toUser, Achievement.acceptedBy == None, Achievement.acceptedAt == None)
        results = await self.session.execute(query.order_by(Achievement.created_at.desc()))
        return results.fetchall()


    async def moderate(self, achievement_moderate: AchievementModerate, moder_uuid: uuid_pkg.UUID) -> None: 
        query_sel = select(Achievement, User).where(Achievement.uuid == achievement_moderate.uuid, User.uuid == Achievement.toUser)
        results = await self.session.execute(query_sel)
        results = results.fetchall()
        achievement = results[0][0]
        student = results[0][1]
        notification_crud = NotificationsCRUD(self.session)
        
        if not achievement_moderate.status: # Reject -> delete
            query = delete(Achievement).where(Achievement.uuid == achievement_moderate.uuid)
            await notification_crud.create_single(NotificationCreate(toUser=student.uuid, type=1, data={"name": achievement.title}))
        else: # Accept -> add points
            query = update(Achievement).where(Achievement.uuid == achievement_moderate.uuid).values(
                acceptedBy=moder_uuid,
                acceptedAt=datetime.datetime.utcnow(),
                points=achievement_moderate.points
            )
            student.rating += achievement_moderate.points
            await notification_crud.create_single(NotificationCreate(toUser=student.uuid, type=0, data={"name": achievement.title, "points": achievement_moderate.points}))
            # query = update(User).where(User.uuid == user_uuid).values(rating=User.rating += 1)
            
        # Commit moderate status
        # TODO: uncomment
        await self.session.execute(query)
        await self.session.commit()
        

    async def get_all_for_user(self, user_uuid: uuid_pkg.UUID, active: bool = True, limit: int = 10000) -> List[Achievement]:
        if active: # Moderated OK
            query = select(*self.columns).where(Achievement.toUser == user_uuid, User.uuid == user_uuid, Achievement.acceptedBy != None, Achievement.acceptedAt != None)
        else: # In moderation queue
            query = select(*self.columns).where(Achievement.toUser == user_uuid, User.uuid == user_uuid, Achievement.acceptedBy == None, Achievement.acceptedAt == None)
        results = await self.session.execute(query.order_by(Achievement.created_at.desc()).join(Achievement).limit(limit))
        return results.fetchall()
    
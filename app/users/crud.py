import uuid as uuid_pkg

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import select, update
from sqlmodel.ext.asyncio.session import AsyncSession
import app.core.security as security
from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate, LeaderboardUser
import sqlalchemy
from typing import List
from app.core.security import verify_password, get_hashed_password


class UsersCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate) -> User:
        values = data.dict()
        if not "role" in values:
            values["role"] = "user"  # Set default role

        # Hash password
        values["password"] = security.get_hashed_password(values["password"])
        try:
            user = User(**values)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except sqlalchemy.exc.IntegrityError as e:  # type: ignore
            err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
            raise HTTPException(
                http_status.HTTP_400_BAD_REQUEST, detail=err_msg)

    async def update(self, user: User, user_data: UserUpdate) -> dict:
        upd_values = {}
        upd_uuid = user.uuid
        if user_data.aboutText != None:
            upd_values["aboutText"] = user_data.aboutText
        if user_data.nickName != None:
            upd_values["nickName"] = user_data.nickName
        if user_data.socialLinks:
            for link in dict(user_data.socialLinks):
                value = dict(user_data.socialLinks)[link]
                if value != None:
                    upd_values[link] = value
        if user_data.techStack != None:
            upd_values["techStack"] = ",".join(user_data.techStack)
        if user_data.password:
            if verify_password(user_data.password.currentPassword, user.password):
                if user_data.password.newPassword == user_data.password.confirmPassword:
                    upd_values["password"] = get_hashed_password(
                        user_data.password.newPassword)
                else:
                    return {"raise": "Confirmation password doesn't match"}
            else:
                return {"raise": "Invalid current password"}
        if user.role in ["teacher", "admin"]:
            if user_data.admin:
                if user_data.uuid:
                    upd_uuid = user_data.uuid
                admin_fields = dict(user_data.admin)
                for field in admin_fields:
                    upd_values[field] = admin_fields[field]

        if upd_values:
            query = update(User).where(
                User.uuid == upd_uuid).values(**upd_values)
            await self.session.execute(query)
            await self.session.commit()
        else:
            return {"raise": "Nothing to update"}

        return upd_values

    async def update_avatar(self, uuid: uuid_pkg.UUID, avatarPath: str):
        query = update(User).where(User.uuid == uuid).values(
            {"avatarPath": avatarPath})
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, id: str | uuid_pkg.UUID) -> User:
        if type(id) == uuid_pkg.UUID:
            query = select(User).where(User.uuid == id)
        else:
            query = select(User).where(User.nickName == id)

        results = await self.session.execute(query)
        user = results.scalar_one_or_none()
        if user is None:
            raise HTTPException(http_status.HTTP_404_NOT_FOUND,
                                detail="User with such uuid/nickname not found")
        return user

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        results = await self.session.execute(query)
        return results.scalar_one_or_none()

    async def get_top_users(self, limit: int) -> List[LeaderboardUser]:
        query = select(User.uuid, User.nickName, User.firstName, User.lastName, User.avatarPath,
                       User.rating).where(User.rating > 0).order_by(User.rating.desc()).limit(limit)
        results = await self.session.execute(query)
        return results.fetchall()

    async def all_(self) -> List[User]:
        results = await self.session.execute(select(User.uuid, User.role, User.rating, User.learningClass, User.aboutText, User.shtpMaintainer, User.groupId,
                                                    User.nickName, User.firstName, User.lastName, User.patronymicName, User.avatarPath, User.telegram,
                                                    User.github, User.stepik, User.kaggle, User.website, User.techStack).order_by(User.created_at.asc()))
        return results.fetchall()

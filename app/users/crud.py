from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select, update
from sqlmodel.ext.asyncio.session import AsyncSession
import app.core.security as security
from app.users.models import User, UserCreate, UserUpdate
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

    async def get(self, uuid: str | UUID) -> User:
        query = select(User).where(User.uuid == uuid)
        results = await self.session.execute(statement=query)
        user = results.scalar_one_or_none()
        if user is None:
            raise HTTPException(http_status.HTTP_404_NOT_FOUND,
                                detail="User with such id not found")
        return user

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        results = await self.session.execute(query)
        return results.scalar_one_or_none()

    async def all_(self) -> List[User]:
        results = await self.session.execute(select(User))
        return results.fetchall()

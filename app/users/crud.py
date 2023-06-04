from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
import app.core.security as security
from app.users.models import User, UserCreate
import sqlalchemy


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

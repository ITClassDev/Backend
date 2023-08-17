from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from fastapi import status as http_status
from app.groups.models import Group
import uuid as uuid_pkg
from sqlalchemy import select, delete
from app.users.models import User
from typing import List


class GroupsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, color: str) -> Group:
        group = Group(name=name, color=color)
        self.session.add(group)
        await self.session.commit()
        await self.session.refresh(group)
        return group

    async def update():
        pass

    async def delete(self, uuid: uuid_pkg.UUID) -> None:
        query = delete(Group).where(Group.uuid == uuid)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, uuid: uuid_pkg.UUID) -> Group:
        query = select(Group).where(Group.uuid == uuid)
        results = await self.session.execute(query)
        user = results.scalar_one_or_none()
        if user is None:
            raise HTTPException(http_status.HTTP_404_NOT_FOUND,
                                detail="Group with such uuid not found")
        return user


    async def all_(self) -> List[Group]:
        query = select(Group.uuid, Group.name, Group.color)
        results = await self.session.execute(query)
        return results.fetchall()
    
    async def get_group_users(self, uuid: uuid_pkg.UUID) -> List[User]:
        query = select(User.uuid).where(User.groupId == uuid)
        results = await self.session.execute(query)
        return results.fetchall()
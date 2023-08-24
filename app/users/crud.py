import uuid as uuid_pkg

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import select, update, delete, or_
from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlalchemy.orm import joinedload
import app.core.security as security
from app.users.models import User
from app.groups.models import Group
from app.users.schemas import UserCreate, UserUpdate, LeaderboardUser, UsersReadAll
import sqlalchemy
from typing import List, Tuple
from app.core.security import verify_password, get_hashed_password
from app.groups.crud import GroupsCRUD
import pandas as pd



class UsersCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate, raise_on_error: bool = True) -> User:
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
            if raise_on_error:
                raise HTTPException(
                    http_status.HTTP_400_BAD_REQUEST, detail=err_msg)
            else:
                return err_msg
        
    async def create_multiple(self, data: pd.DataFrame) -> Tuple[List[User], List[str]]:
        '''
        Return's list of created users and list of errors
        '''
        groups_crud = GroupsCRUD(self.session)
        all_groups = await groups_crud.all_()
        groups_map = {gr.name: gr.uuid for gr in all_groups}
        errors = []
        created = []
        for _, row in data.iterrows():
            try:
                user = User(firstName=row["firstName"], lastName=row["lastName"], email=row["email"], role=row["role"], password=row["password"], learningClass=row["learningClass"], groupId=groups_map[row["groupName"]])
                self.session.add(user)
                await self.session.commit()
                await self.session.refresh(user)
                created.append(user)

            except sqlalchemy.exc.IntegrityError as e:  # type: ignore
                err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
                errors.append(f"User email: {row['email']} - {err_msg}")
            except Exception as e: # Generic error
                errors.append(f"User email: {row['email']} - {str(e)[:50]}")
        
        return created, errors
    
    async def cascade_delete(self, uuid: uuid_pkg.UUID) -> None:
        '''
        It is dangerous method!
        It will delete user and all it's information, like ahievements, apps, projects and e.t.c
        '''
        
        query = delete(User).where(User.uuid == uuid)
        
        await self.session.execute(query)
        await self.session.commit()


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
            query = select(User, Group).where(User.uuid == id).join(User.group)
        else:
            query = select(User, Group).where(User.nickName == id).join(User.group)

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
        results = await self.session.execute(select(User.firstName, User.lastName, User.groupId, User.uuid, User.avatarPath, User.nickName, User.learningClass).order_by(User.created_at.asc()))
        return results.fetchall()
    
    async def search(self, query: str) -> List[UsersReadAll]:
        query = select(User.uuid, User.firstName, User.lastName, User.avatarPath, User.groupId, User.learningClass, User.nickName).filter(or_(
            User.firstName.like(f"%{query}%"),
            User.lastName.like(f"%{query}%")
        ))
        results = await self.session.execute(query)
        return results.fetchall()

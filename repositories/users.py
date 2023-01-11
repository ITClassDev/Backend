from db.users import users
from db.user_groups import user_groups
from .base import BaseRepository
from models.user import User, UserIn, UserUpdate
from typing import List
from sqlalchemy import select


class UserRepository(BaseRepository):
    async def get_user_info(self, id: int) -> User:
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query)
        if not user:
            return None

        return User.parse_obj(user)

    async def get_all_users(self) -> List[User]:
        query = select(users.c.id, users.c.firstName, users.c.lastName, users.c.userAvatarPath, users.c.groupId, user_groups.c.name.label("groupName")).where(user_groups.c.id == users.c.groupId).order_by(users.c.id.asc())
        return await self.database.fetch_all(query)

    async def get_user_by_email(self, email: str) -> User:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if not user: return None
        return User.parse_obj(user)

    async def update(self, id: int, user_data: UserUpdate) -> None:
        upd_values = {**user_data.dict()}
        query = users.update().where(users.c.id == id).values(**upd_values)
        await self.database.execute(query)

    async def update_avatar(self, id: int, avatar: str) -> User:
        query = users.update().where(users.c.id == id).values(
            {"userAvatarPath": avatar})
        await self.database.execute(query)

    async def update_about_text(self, id: int, new_about_text: str) -> None:
        query = users.update().where(users.c.id == id).values({"userAboutText": new_about_text})
        await self.database.execute(query)

    async def get_top(self, count: int) -> List[User]:
        query = select(users.c.id, users.c.firstName, users.c.lastName, users.c.userAvatarPath,
                       users.c.rating).order_by(users.c.rating.desc()).limit(count)
        return await self.database.fetch_all(query)

    async def create(self, user: UserIn):
        pass



from db.users import users
from .base import BaseRepository
from models.user import User, UserIn


class UserRepository(BaseRepository):
    async def get_user_info(self, id: int) -> User:
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def get_user_by_email(self, email: str) -> User:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def update_avatar(self, id: int, avatar: str) -> User:
        query = users.update().where(users.c.id == id).values(
            {"userAvatarPath": avatar})
        await self.database.execute(query)

    async def create(self, user: UserIn):
        pass
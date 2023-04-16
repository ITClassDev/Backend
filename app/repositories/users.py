from db.users import users
from db.user_groups import user_groups
from .base import BaseRepository
from models.user import User, UserIn, UserUpdate, SocialLinksIn
from typing import List
from sqlalchemy import select
from core.security import hash_password, verify_password
import asyncpg


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

    async def update(self, user: User, user_data: UserUpdate) -> None:
        upd_values = {}
        if user_data.aboutText:
            upd_values["userAboutText"] = user_data.aboutText
        if user_data.socialLinks:
            for link in dict(user_data.socialLinks):
                value = dict(user_data.socialLinks)[link]
                if value:
                    upd_values[link] = value
        if user_data.techStack:
            upd_values["techStack"] = ",".join(user_data.techStack)
        if user_data.password:
            if verify_password(user_data.password.currentPassword, user.hashedPassword):
                if user_data.password.newPassword == user_data.password.confirmPassword:
                    upd_values["hashedPassword"] = hash_password(user_data.password.newPassword)
                else:
                    return {"raise": "Confirmation password doesn't match"}
            else:
                return {"raise": "Invalid current password"}
        
        if upd_values:
            query = users.update().where(users.c.id == user.id).values(**upd_values)
            await self.database.execute(query)
        else:
            return {"raise": "Nothing to update"}
        
        return {}

    async def update_avatar(self, id: int, avatar: str) -> User:
        query = users.update().where(users.c.id == id).values(
            {"userAvatarPath": avatar})
        await self.database.execute(query)
    
    async def update_social_links(self, social_links: SocialLinksIn, user_id: int) -> None:
        data = {
            "userGithub": social_links.github,
            "userTelegram": social_links.telegram,
            "userStepik": social_links.stepik,
            "userKaggle": social_links.kaggle,
            "userWebsite": social_links.website
        }
        query = users.update().where(users.c.id == user_id).values(**data)
        await self.database.execute(query)

    async def update_about_text(self, id: int, new_about_text: str) -> None:
        query = users.update().where(users.c.id == id).values({"userAboutText": new_about_text})
        await self.database.execute(query)

    async def get_top(self, count: int) -> List[User]:
        query = select(users.c.id, users.c.firstName, users.c.lastName, users.c.userAvatarPath,
                       users.c.rating).order_by(users.c.rating.desc()).limit(count)
        return await self.database.fetch_all(query)

    async def create(self, user: UserIn) -> int:
        userObj = User(email=user.email, firstName=user.firstName, lastName=user.lastName, userRole=user.userRole, hashedPassword=hash_password(user.password), learningClass=user.learningClass, groupId=user.groupId, rating=0, userAvatarPath="default.png")
        values = {**userObj.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        user_id = await self.database.execute(query)
        return user_id

    async def update_password(self, user_id: int, new_password: str) -> None:
        query = users.update().where(users.c.id == user_id).values(hashedPassword=hash_password(new_password))
        return await self.database.execute(query)

    async def update_tech_stack(self, user_id: int, new_tech_stack: list) -> None:
        new_tech_stack_string = ",".join(new_tech_stack)
        query = users.update().where(users.c.id == user_id).values(techStack=new_tech_stack_string)
        return await self.database.execute(query)

    async def create_multiple(self, users_list: list) -> List[int]:
        created_ids = []
        failed_to_create = []
        for user in users_list:
            userObj = User(firstName=user[0], lastName=user[1], email=user[2], userRole=user[3], hashedPassword=hash_password(user[4]), learningClass=user[5], groupId=user[6])
            values = {**userObj.dict()}
            values.pop("id", None)
            query = users.insert().values(**values)
            try:
                created_ids.append(await self.database.execute(query))
            except asyncpg.exceptions.UniqueViolationError:
                failed_to_create.append(user[2])
        return created_ids, failed_to_create
    
    async def delete(self, id: int) -> None:
        await self.database.execute(users.delete().where(users.c.id == id)) 

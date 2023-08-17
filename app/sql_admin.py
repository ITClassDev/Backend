from typing import Optional
from sqladmin import Admin, ModelView
from app.core.db import async_engine
from app.core.security import verify_password
from app.users.models import User
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from app.users.models import User
from app.groups.models import Group
from app.notifications.models import Notification
from app.achievements.models import Achievement


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()

        email, password = form["username"], form["password"]
        async_session = sessionmaker(
            async_engine, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            users_cnt = await session.execute(select(User))

            if not len(users_cnt.fetchall()):  # ShTP Backend Run on empty db
                request.session.update({"token": "shdfhsdf" * 50})
                return True
            res = await session.execute(
                select(User).where(User.email == email)
            )
            res = res.first()
            if res:
                user = res[0]
                if user.role == "admin" or user.shtpMaintainer:
                    if verify_password(password, user.password):
                        request.session.update({"token": "TOKEN"})
                        return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # TODO check the token in depth


class UserAdmin(ModelView, model=User):
    column_list = [User.uuid, User.email, User.firstName, User.lastName, User.group]


class GroupAdmin(ModelView, model=Group):
    column_list = [Group.uuid, Group.name, Group.color]

class NotificationAdmin(ModelView, model=Notification):
    column_list = [Notification.uuid, Notification.type, Notification.data]

class AchievementAdmin(ModelView, model=Achievement):
    column_list = [Achievement.uuid, Achievement.title, Achievement.description]


def create(app, secret_key):
    authentication_backend = AdminAuth(secret_key=secret_key)
    sql_admin = Admin(app, async_engine,
                      authentication_backend=authentication_backend, base_url="/db_admin")
    sql_admin.add_view(UserAdmin)
    sql_admin.add_view(GroupAdmin)
    sql_admin.add_view(NotificationAdmin)
    sql_admin.add_view(AchievementAdmin)
    return sql_admin

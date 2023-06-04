from fastapi import Depends, HTTPException
from fastapi import status as http_status
from app.users.dependencies import get_users_crud
from app.users.models import User
from app.users.crud import UsersCRUD
from fastapi_jwt_auth import AuthJWT


async def get_current_user(Authorize: AuthJWT = Depends(), users: UsersCRUD = Depends(get_users_crud)):
    Authorize.jwt_required()
    email = Authorize.get_jwt_subject()
    return await users.get_by_email(str(email))


async def moder_role_access(Authorize: AuthJWT = Depends(), users: UsersCRUD = Depends(get_users_crud)):
    Authorize.jwt_required()
    email = Authorize.get_jwt_subject()
    user = await users.get_by_email(str(email))
    if user.role in ["moderator", "admin"]:
        return user
    raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN,
                        detail="You can't access this endpoint!")

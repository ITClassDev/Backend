from fastapi import Depends, HTTPException
from fastapi import status as http_status
from app.users.dependencies import get_users_crud
from app.users.models import User
from app.users.crud import UsersCRUD
from fastapi_jwt_auth import AuthJWT
from typing import List


async def get_current_user(Authorize: AuthJWT = Depends(), users: UsersCRUD = Depends(get_users_crud)):
    Authorize.jwt_required()
    email = Authorize.get_jwt_subject()
    return await users.get_by_email(str(email))


async def access_by_role(acceptable_roles: List[str], Authorize: AuthJWT, users: UsersCRUD) -> User:
    Authorize.jwt_required()
    email = Authorize.get_jwt_subject()
    user = await users.get_by_email(str(email))
    if user.role in acceptable_roles:
        return user
    raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN,
                        detail="You can't access this endpoint!")


async def atleast_teacher_access(Authorize: AuthJWT = Depends(), users: UsersCRUD = Depends(get_users_crud)) -> User:
    return await access_by_role(["teacher", "admin"], Authorize, users)


async def only_admin_access(Authorize: AuthJWT = Depends(), users: UsersCRUD = Depends(get_users_crud)) -> User:
    return await access_by_role(["admin"], Authorize, users)

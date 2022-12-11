from repositories.users import UserRepository
from repositories.achievements import AchievementRepository
from repositories.apps import AppsRepository
from db.base import database
from fastapi import Depends, HTTPException, status
from core.security import JWTBearer, decode_access_token
from models.user import User


def get_user_repository() -> UserRepository:
    return UserRepository(database)

def get_achievement_repository() -> AchievementRepository:
    return AchievementRepository(database)

def get_apps_repository() -> AppsRepository:
    return AppsRepository(database)
    

async def get_current_user(
    users: UserRepository = Depends(get_user_repository),
    token: str = Depends(JWTBearer()),
) -> User:

    cred_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    email: str = payload.get("sub")
    if email is None:
        raise cred_exception
    user = await users.get_user_by_email(email=email)
    if user is None:
        return cred_exception
    return user

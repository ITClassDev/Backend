from fastapi import APIRouter, Depends, HTTPException, status, Request
from models.token import Token, Login
from repositories.users import UserRepository
from repositories.notifications import NotificationRepository
from models.user import User
from core.security import verify_password, create_access_token
from .depends import get_user_repository, get_current_user, get_notification_repository

router = APIRouter()


@router.post("/login", response_model=Token)
async def auth_login(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_user_by_email(login.email)
    if user is None or not verify_password(login.password, user.hashedPassword):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect pair of login && password")
    token = create_access_token({"sub": user.email})
    return Token(accessToken=token, tokenType="Bearer")

# Endpoint to get current user data by access token
@router.get("/me")
async def check_auth(current_user: User = Depends(get_current_user), notifications: NotificationRepository = Depends(get_notification_repository)):
    if current_user:
        user = dict(current_user)
        user["new_notifications"] = await notifications.check_active_notifications(current_user.id)
        user_data = user
        user_data.pop("hashedPassword")
        user_data.pop("email")
        return {"status": True, "user": user_data}
    return {"status": False}
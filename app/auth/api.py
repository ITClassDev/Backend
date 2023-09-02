from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from fastapi_jwt_auth import AuthJWT
from app.users.schemas import UserLogin, UserRead
from app.users.models import User
from app.users.dependencies import get_users_crud
from app.notifications.dependencies import get_notifications_crud
from app.auth.dependencies import get_current_user
from app.users.crud import UsersCRUD
from app.notifications.crud import NotificationsCRUD
from app.core.security import verify_password
from app.auth.schemas import AuthData, NewAccessToken

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user), notifications: NotificationsCRUD = Depends(get_notifications_crud)):
    if current_user:
        values = current_user.dict()
        values["group"] = current_user.group.dict()
        values["newNotifications"] = len(await notifications.get_active_notifications(current_user.uuid)) > 0
        return values
    raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail="No login")


@router.post("/login", response_model=AuthData)
async def login(auth_data: UserLogin, Authorize: AuthJWT = Depends(), users: UsersCRUD = Depends(get_users_crud)):
    user = await users.get_by_email(auth_data.email)
    if user:
        if verify_password(auth_data.password, user.password):
            access_token = Authorize.create_access_token(
                subject=auth_data.email)
            refresh_token = Authorize.create_refresh_token(
                subject=auth_data.email)
            return {"accessToken": access_token, "refreshToken": refresh_token}

    raise HTTPException(http_status.HTTP_403_FORBIDDEN,
                        detail="Invalid pair login && password")


@router.post("/refresh", response_model=NewAccessToken)
async def refresh_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"accessToken": new_access_token}

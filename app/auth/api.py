from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from fastapi_jwt_auth import AuthJWT
from app.users.models import UserLogin, UserRead, User
from app.users.dependencies import get_users_crud
from app.auth.dependencies import get_current_user
from app.users.crud import UsersCRUD

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/login")
async def login(user: UserLogin, Authorize: AuthJWT = Depends(), users: UsersCRUD = Depends(get_users_crud)):
    if await users.get_by_email(user.email):
        access_token = Authorize.create_access_token(subject=user.email)
        refresh_token = Authorize.create_refresh_token(subject=user.email)
        return {"access_token": access_token, "refresh_token": refresh_token}
    else:
        raise HTTPException(http_status.HTTP_403_FORBIDDEN,
                            detail="No user with such email")


@router.post("/refresh")
async def refresh_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
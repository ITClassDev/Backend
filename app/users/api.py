from fastapi import APIRouter, Depends
from app.users.crud import UsersCRUD
from app.users.dependencies import get_users_crud
from app.users.models import UserCreate, UserRead, User
from app.auth.dependencies import get_current_user, moder_role_access
import uuid as uuid_pkg

router = APIRouter()


@router.put("", response_model=UserRead)
async def create_user(user: UserCreate, users: UsersCRUD = Depends(get_users_crud)):
    return await users.create(user)


@router.patch("", response_model=UserRead)
async def update_user(user: User = Depends(get_current_user)):
    pass

# @router.get("/only_moder_test")
# def moder_test(user: User = Depends(moder_role_access)):
#     return user


@router.get("/{user_uuid}", response_model=UserRead)
async def get_user_by_id(user_uuid: uuid_pkg.UUID, users: UsersCRUD = Depends(get_users_crud)):
    return await users.get(user_uuid)
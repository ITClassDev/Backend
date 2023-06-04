from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status
from app.users.crud import UsersCRUD
from typing import List
from app.users.dependencies import get_users_crud
from app.users.models import UserCreate, UserRead, User, UserUpdate
from app.auth.dependencies import get_current_user, atleast_teacher_access
import uuid as uuid_pkg

router = APIRouter()


@router.put("", response_model=UserRead)
async def create_user(user: UserCreate, users: UsersCRUD = Depends(get_users_crud)):
    return await users.create(user)


@router.patch("")
async def update_user_info(update_data: UserUpdate, current_user: User = Depends(get_current_user), users: UsersCRUD = Depends(get_users_crud)):
    result = await users.update(current_user, update_data)
    if "raise" in result:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=result["raise"])
    else:
        return {**result}

# @router.get("/only_moder_test")
# def moder_test(user: User = Depends(moder_role_access)):
#     return user


@router.get("/{user_uuid}", response_model=UserRead)
async def get_user_by_id(user_uuid: uuid_pkg.UUID, users: UsersCRUD = Depends(get_users_crud)):
    return await users.get(user_uuid)


@router.get("", response_model=List[UserRead])
async def get_all_users(users: UsersCRUD = Depends(get_users_crud), current_user: User = Depends(atleast_teacher_access)):
    res = await users.all_()
    print(res)
    return res

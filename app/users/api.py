from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi import status as http_status
from app.users.crud import UsersCRUD
from typing import List
from app.users.dependencies import get_users_crud
from app.users.schemas import UserCreate, UserRead, UserUpdate, LeaderboardUser, UserUpdateResponse, MultipleCreate
from app.users.models import User
from app.auth.dependencies import get_current_user, atleast_teacher_access
import uuid as uuid_pkg
from app import settings
import os
from app.core.files import upload_file
from app.users.schemas import UpdateAvatarResponse, UsersReadAll
import pandas as pd

router = APIRouter()


@router.get("", response_model=List[UsersReadAll])
async def get_all_users(users: UsersCRUD = Depends(get_users_crud), current_user: User = Depends(atleast_teacher_access)):
    a = await users.all_()
    return a


@router.put("", response_model=UserRead)
async def create_user(user: UserCreate, users: UsersCRUD = Depends(get_users_crud)):
    return await users.create(user)


@router.put("/csv", response_model=MultipleCreate)
async def create_multiple_users_from_csv(csv_file: UploadFile, users: UsersCRUD = Depends(get_users_crud), current_user: User = Depends(atleast_teacher_access)):
    csv_content = await upload_file(csv_file, ["csv"], write=False) # In RAM processing
    csv_content = csv_content["file_content"].decode("utf-8").strip()
    df = pd.DataFrame([row.split(',') for row in csv_content.split('\n')[1:]], 
                   columns=["firstName", "lastName", "email", "role", "password", "learningClass", "groupName"])
    users_created, errors = await users.create_multiple(df)
    return MultipleCreate(users=users_created, errors=errors)
    


@router.delete("/{user_id}")
async def delete_user(user_uuid: uuid_pkg.UUID, current_user: User = Depends(atleast_teacher_access), users: UsersCRUD = Depends(get_users_crud)):
    return await users.cascade_delete(user_uuid)


@router.patch("", response_model=UserUpdateResponse)
async def update_user_info(update_data: UserUpdate, current_user: User = Depends(get_current_user), users: UsersCRUD = Depends(get_users_crud)):
    result = await users.update(current_user, update_data)
    if "raise" in result:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST, detail=result["raise"])
    else:
        return {**result}


@router.patch("/avatar", response_model=UpdateAvatarResponse)
async def update_avatar(avatar: UploadFile, current_user: User = Depends(get_current_user), users: UsersCRUD = Depends(get_users_crud)):
    allowed_extensions = ["png", "jpg", "gif", "jpeg"]
    try:
        if current_user.avatarPath != "default.png":
            os.remove(os.path.join(settings.user_storage,
                      "avatars", current_user.avatarPath))
    except FileNotFoundError:
        pass

    uploaded_avatar = await upload_file(avatar, allowed_extensions, os.path.join(settings.user_storage, "avatars"), md5_name=True)
    if uploaded_avatar["status"]:
        await users.update_avatar(current_user.uuid, uploaded_avatar["file_name"])
        return {"avatar": uploaded_avatar["file_name"]}
    else:
        raise HTTPException(http_status.HTTP_400_BAD_REQUEST,
                            detail=uploaded_avatar["info"])


@router.get("/leaderboard", response_model=List[LeaderboardUser])
async def get_leaderboard(limit: int = 10, users: UsersCRUD = Depends(get_users_crud)):
    resp = await users.get_top_users(limit)
    return resp


@router.get("/{id}", response_model=UserRead)
async def get_user_by_uuid_or_nick(id: uuid_pkg.UUID | str, users: UsersCRUD = Depends(get_users_crud)):
    return await users.get(id)

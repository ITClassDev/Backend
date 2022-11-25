from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, File, UploadFile
from repositories.users import UserRepository
from models.user import User, UserIn
from .depends import get_user_repository, get_current_user
import pbs.main_pb2 as MainBuffer
from core.utils.variables import NON_AUTH_PACKET
from core.utils.files import upload_file
from core.config import USERS_STORAGE
import os

router = APIRouter()


@router.get("/{user_id}/info")
async def get_user_info(user_id: int, users: UserRepository = Depends(get_user_repository)):
    data = await users.get_user_info(int(user_id))
    return_data = {"status": False, "info": "no user with such id"}
    if data:
        return_data = {"status": True, "firstName": data.firstName, "lastName": data.lastName, "middleName": data.middleName,
                       "email": data.email, "rating": data.rating, "role": data.userRole, "telegramLink": data.userTelegram, "githubLink": data.userGithub, "stepikLink": data.userStepik, "kaggleLink": data.userKaggle, "avatarPath": data.userAvatarPath}
    return return_data


@router.post("/create_user")
async def create_user(new_user: UserIn, current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository)):
    if current_user.userRole == 1:  # Is admin
        return await users.create(u=new_user)
    else:
        pass


@router.post("/upload_avatar")
async def upload_file_test(current_user: User = Depends(get_current_user), request: Request = Request, file: UploadFile = None, users: UserRepository = Depends(get_user_repository)):
    if current_user:
        allowed_extensions = ["png", "jpg"]
        uploaded_avatar =  await upload_file(file, allowed_extensions, os.path.join(USERS_STORAGE, "avatars"), custom_name=f"{current_user.id}_avatar")
        if uploaded_avatar["status"]:
            await users.update_avatar(current_user.id, uploaded_avatar["file_name"])
            return {"status": True, "avatar": uploaded_avatar["file_name"]}
        else:
            return {"status": False, "info": uploaded_avatar["info"]}
    return NON_AUTH_PACKET


# Dev
@router.get("/test_auth")
async def test_auth(current_user: User = Depends(get_current_user)):
    if current_user:
        return {"status": True, "userId": current_user.id, "userFname": current_user.firstName}
    return NON_AUTH_PACKET


@router.post("/{user_id}/update_profile")
async def update_user_info(current_user: User = Depends(get_current_user)):
    if current_user:
        print(current_user.id)
    return NON_AUTH_PACKET

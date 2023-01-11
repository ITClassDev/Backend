from fastapi import APIRouter, Depends, UploadFile
from repositories.users import UserRepository
from repositories.apps import  AppsRepository
from repositories.notifications import NotificationRepository
from models.user import User, UserIn, AboutText, UserUpdate
from .depends import get_user_repository, get_current_user, get_apps_repository, get_notification_repository
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
        return_data = {"status": True, "firstName": data.firstName, "lastName": data.lastName,
                       "middleName": data.middleName,
                       "email": data.email, "rating": data.rating, "userRole": data.userRole,
                       "userTelegram": data.userTelegram, "userGithub": data.userGithub, "userStepik": data.userStepik,
                       "userKaggle": data.userKaggle, "userAvatarPath": data.userAvatarPath,
                       "userAboutText": data.userAboutText, "learningClass": data.learningClass, "techStack": data.techStack}
    return return_data


@router.put("/create_user")
async def create_user(new_user: UserIn, current_user: User = Depends(get_current_user),
                      users: UserRepository = Depends(get_user_repository)):
    if current_user.userRole > 0:  # Is admin
        created_user_id = await users.create(new_user)
        return {"user_id": created_user_id}
    else:
        return NON_AUTH_PACKET


@router.patch("/upload_avatar")
async def upload_file_test(current_user: User = Depends(get_current_user), file: UploadFile = None,
                           users: UserRepository = Depends(get_user_repository)):
    if current_user:
        allowed_extensions = ["png", "jpg"]  # no gifs for now
        uploaded_avatar = await upload_file(file, allowed_extensions, os.path.join(USERS_STORAGE, "avatars"),
                                            custom_name=f"{current_user.id}_avatar")
        if uploaded_avatar["status"]:
            await users.update_avatar(current_user.id, uploaded_avatar["file_name"])
            return {"status": True, "avatar": uploaded_avatar["file_name"]}
        else:
            return {"status": False, "info": uploaded_avatar["info"]}
    return NON_AUTH_PACKET


@router.patch("/{user_id}/update_profile")
async def update_user_info(update_data: UserUpdate, current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository)):
    if current_user:
        await users.update(current_user.id, update_data)
        return 1

    return NON_AUTH_PACKET


@router.patch("/update_about_text")
async def update_avatar(about_text: AboutText, current_user: User = Depends(get_current_user),
                        users: UserRepository = Depends(get_user_repository)):
    if current_user:
        await users.update_about_text(current_user.id, about_text.about_text)
        return {"status": True, "new_about": about_text.about_text}
    return NON_AUTH_PACKET

#@router.post("/update_info")


@router.get("/get_leaderboard")
async def get_leaderboard(limit: int = 10, users: UserRepository = Depends(get_user_repository)):
    return await users.get_top(limit)


@router.get("/my_apps")
async def get_my_apps(current_user: User = Depends(get_current_user), apps: AppsRepository = Depends(get_apps_repository)):
    if current_user:
        return await apps.get_for_user(current_user.id)
    return NON_AUTH_PACKET

@router.get("/my_notifications")
async def get_my_notifications(current_user: User = Depends(get_current_user), notifications: NotificationRepository = Depends(get_notification_repository)):
    data = await notifications.get_all_for_user(current_user.id)
    return data
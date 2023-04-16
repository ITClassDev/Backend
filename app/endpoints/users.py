from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from repositories.user_groups import UserGroupsRepository
from repositories.users import UserRepository
from repositories.apps import AppsRepository
from repositories.notifications import NotificationRepository
from models.user import User, UserIn, AboutText, UserUpdate, SocialLinksIn, UpdatePassword, UpdateTechStack
from .depends import get_user_repository, get_current_user, get_apps_repository, get_notification_repository, get_user_groups_repository
from core.utils.files import upload_file
from core.config import USERS_STORAGE, ERROR_TEXTS

import os

router = APIRouter()

@router.get("/")
async def get_all_users(current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository), user_groups: UserGroupsRepository = Depends(get_user_groups_repository)):
    if current_user.userRole > 0:
        all_users = await users.get_all_users()
        all_user_groups = await user_groups.get_all()
        return {"users": all_users, "userGroups": all_user_groups}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TEXTS.low_permissions)


@router.get("/{user_id}")
async def get_user_info(user_id: int, users: UserRepository = Depends(get_user_repository)):
    data = await users.get_user_info(int(user_id))
    if data:
        # Return only public data
        return {"status": True, "firstName": data.firstName, "lastName": data.lastName,
                "middleName": data.middleName, "rating": data.rating, "userRole": data.userRole,
                "userTelegram": data.userTelegram, "userGithub": data.userGithub, "userStepik": data.userStepik,
                "userKaggle": data.userKaggle, "userWebsite": data.userWebsite, "userAvatarPath": data.userAvatarPath,
                "userAboutText": data.userAboutText, "learningClass": data.learningClass, "techStack": data.techStack}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No user with such id")

@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository)):
    if current_user.userRole == 2: # Only for super admin
        await users.delete(user_id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=ERROR_TEXTS.low_permissions)


@router.put("/")
async def create_user(new_user: UserIn, current_user: User = Depends(get_current_user),
                      users: UserRepository = Depends(get_user_repository)):
    if current_user.userRole > 0:  # Is admin
        created_user_id = await users.create(new_user)
        return {"userId": created_user_id}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TEXTS.low_permissions) # FIXIT MAKE text mapping

@router.put("/from_csv")
async def multiple_users_creation(file: UploadFile, users: UserRepository = Depends(get_user_repository), current_user: User = Depends(get_current_user)):
    if current_user.userRole > 0:
        csv_content = await upload_file(file, ["csv"], write=False)
        csv_content = csv_content["file_content"].decode("utf-8")
        users_data = [list(map(str.strip, x.split(','))) for x in csv_content.split('\n')[1:-1]]
        created, skipped = await users.create_multiple(users_data)
        return {"created": created, "skipped": skipped}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TEXTS.low_permissions)


@router.patch("/upload_avatar")
async def upload_file_test(file: UploadFile, current_user: User = Depends(get_current_user),
                           users: UserRepository = Depends(get_user_repository)):
    allowed_extensions = ["png", "jpg"]  # no gifs for now
    uploaded_avatar = await upload_file(file, allowed_extensions, os.path.join(USERS_STORAGE, "avatars"),
                                        custom_name=f"{current_user.id}_avatar")
    if uploaded_avatar["status"]:
        await users.update_avatar(current_user.id, uploaded_avatar["file_name"])
        return {"status": True, "avatar": uploaded_avatar["file_name"]}
    else:
        return {"status": False, "info": uploaded_avatar["info"]}


@router.patch("/")
async def update_user_info(update_data: UserUpdate, current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository)):
    result = await users.update(current_user, update_data)
    if "raise" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["raise"])
    else:
        return {"status": True}


@router.patch("/update/about")
async def update_avatar(about_text: AboutText, current_user: User = Depends(get_current_user),
                        users: UserRepository = Depends(get_user_repository)):

    await users.update_about_text(current_user.id, about_text.about_text)
    return {"status": True, "newAbout": about_text.about_text}


@router.patch("/update/social")
async def update_social(social_links: SocialLinksIn, current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository)):
    await users.update_social_links(social_links, current_user.id)
    return {"status": "True"}


# @router.patch("/update/password")
# async def update_password(update_password: UpdatePassword, current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository)):
#     if verify_password(update_password.current_password, current_user.hashedPassword):
#         if update_password.new_password == update_password.confirm_password:
#             await users.update_password(current_user.id, update_password.new_password)
#             return {"status": True}
#         else:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                                 detail="Confirmation password doesn't match")
#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail="Invalid current password")

@router.put("/groups/add")
async def add_groups(current_user: User = Depends(get_current_user)):
    pass


@router.patch("/update/tech_stack")
async def update_tech_stack(new_tech_stack: UpdateTechStack, current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository)):
    await users.update_tech_stack(current_user.id, new_tech_stack.tech_stack)
    return {"status": True}


@router.get("/get_leaderboard")
async def get_leaderboard(limit: int = 10, users: UserRepository = Depends(get_user_repository)):
    return await users.get_top(limit)


@router.get("/my_apps")
async def get_my_apps(current_user: User = Depends(get_current_user), apps: AppsRepository = Depends(get_apps_repository)):
    return await apps.get_for_user(current_user.id)


@router.get("/my_notifications")
async def get_my_notifications(current_user: User = Depends(get_current_user), notifications: NotificationRepository = Depends(get_notification_repository)):
    data = await notifications.get_all_for_user(current_user.id)
    return data



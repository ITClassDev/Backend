from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi import status as http_status
from app.auth.dependencies import get_current_user
from app.users.models import User
from app.achievements.crud import AchievementsCRUD
from app.achievements.dependencies import get_achievements_crud
from app.achievements.schemas import AchievementCreate, AchievementRead
from app import settings
import os
from typing import List
from app.core.files import upload_file

router = APIRouter()


@router.get("", response_model=List[AchievementRead])
async def get_current_user_achievements(current_user: User = Depends(get_current_user), achievements: AchievementsCRUD = Depends(get_achievements_crud)):
    return await achievements.get_all_for_user(current_user.uuid)


@router.put("")
async def add_achievements(achievement: AchievementCreate, confirmFile: UploadFile, current_user: User = Depends(get_current_user), achievements: AchievementsCRUD = Depends(get_achievements_crud)):
    uploaded_image = await upload_file(confirmFile, ["png", "jpg", "pdf", "jpeg"], os.path.join(settings.user_storage, "achievements"))
    if uploaded_image["status"]:
        return await achievements.create(achievement, current_user.uuid, uploaded_image["file_name"])
    else:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Can't upload such file; Check extension: [pdf, png, jpg, jpeg]")


@router.patch("/moderate")
async def accept_achievement():
    pass


@router.get("/pending")
async def get_user_pending_achievements(current_user: User = Depends(get_current_user), achievements: AchievementsCRUD = Depends(get_achievements_crud)):
    return await achievements.get_all_for_user(current_user.uuid, active=False)


@router.get("/queue")
async def admin_get_all_achievements_queue():
    pass

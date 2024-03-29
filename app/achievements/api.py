from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi import status as http_status
import uuid as uuid_pkg
from app.auth.dependencies import get_current_user, atleast_teacher_access
from app.users.models import User
from app.achievements.crud import AchievementsCRUD
from app.achievements.dependencies import get_achievements_crud
from app.achievements.schemas import AchievementCreate, AchievementRead, AchievementModerate
from app import settings
import os
from typing import List
from app.core.files import upload_file, create_archive

router = APIRouter()


@router.get("", response_model=List[AchievementRead])
async def get_current_user_achievements(current_user: User = Depends(get_current_user), achievements: AchievementsCRUD = Depends(get_achievements_crud)):
    return await achievements.get_all_for_user(current_user.uuid)

@router.put("", response_model=AchievementRead)
async def add_achievements(achievement: AchievementCreate, confirmFile: UploadFile, current_user: User = Depends(get_current_user), achievements: AchievementsCRUD = Depends(get_achievements_crud)):
    uploaded_image = await upload_file(confirmFile, ["png", "jpg", "pdf", "jpeg"], os.path.join(settings.user_storage, "achievements"))
    if uploaded_image["status"]:
        return await achievements.create(achievement, current_user.uuid, uploaded_image["file_name"])
    else:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Can't upload such file; Check extension: [pdf, png, jpg, jpeg]")

@router.get("/export")
async def export_current_user_achievements(current_user: User = Depends(get_current_user), achievements: AchievementsCRUD = Depends(get_achievements_crud)):
    if current_user.role == "student":
        all_ = await achievements.get_all_for_user(current_user.uuid, active=True, limit=10000)
        if len(all_):
            attachments = []
            md_text = ""
            for i in all_:
                attachments.append(i.attachmentName)
                md_text += f"## {i.title}\nУченик: {current_user.firstName} {current_user.lastName}\n\nОписание: {i.description}\n\nБаллы: {i.points}\n\nДата: {i.acceptedAt}\n\nНазвание файла диплома: {i.attachmentName}\n\n"
            result_archive = await create_archive(os.path.join(settings.user_storage, "achievements"), attachments, [{"name": "achievements.md", "content": md_text}])
            response = StreamingResponse(
                    iter([result_archive.getvalue()]),
                    media_type="application/x-zip-compressed",
                    headers = {"Content-Disposition":f"attachment;filename=achievements_dump.zip",
                                "Content-Length": str(result_archive.getbuffer().nbytes)}
                )
            return response
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="You don't have achievements yet!")
    raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail="Only for students")

@router.patch("/moderate", response_model=None)
async def moderate_achievement(achievement: AchievementModerate, current_user: User = Depends(atleast_teacher_access), achievements: AchievementsCRUD = Depends(get_achievements_crud)):
    await achievements.moderate(achievement, current_user.uuid)


@router.get("/pending", response_model=List[AchievementRead])
async def get_user_pending_achievements(current_user: User = Depends(get_current_user), achievements: AchievementsCRUD = Depends(get_achievements_crud)):
    return await achievements.get_all_for_user(current_user.uuid, active=False)


@router.get("/queue", response_model=List[AchievementRead])
async def admin_get_all_achievements_queue(_: User = Depends(atleast_teacher_access), achievements: AchievementsCRUD = Depends(get_achievements_crud)):
    return await achievements.all_queue()

@router.get("/user/{uuid}", response_model=List[AchievementRead])
async def get_users_achievements(uuid: uuid_pkg.UUID, achievements: AchievementsCRUD = Depends(get_achievements_crud)):
    return await achievements.get_all_for_user(uuid, active=True, limit=6)
from fastapi import APIRouter, Depends
from app.notifications.crud import NotificationsCRUD
from app.notifications.schemas import NotificationCreate, NotificationRead
from app.notifications.models import Notification
from app.notifications.dependencies import get_notifications_crud
from app.auth.dependencies import get_current_user, atleast_teacher_access
from app.users.models import User
from typing import List

router = APIRouter()


@router.put("")
async def send_notification(notification: NotificationCreate, notifications: NotificationsCRUD = Depends(get_notifications_crud), current_user: User = Depends(atleast_teacher_access)):
    return await notifications.create(notification)

@router.get("", response_model=List[Notification])
async def notification_polling(notifications: NotificationsCRUD = Depends(get_notifications_crud), current_user: User = Depends(get_current_user)):
    data = await notifications.get_active_notifications(current_user.uuid)
    await notifications.set_readed(current_user.uuid)
    return data

@router.get("/all", response_model=List[NotificationRead])
async def all_my_notifications(notifications: NotificationsCRUD = Depends(get_notifications_crud), current_user: User = Depends(get_current_user)):
    await notifications.set_readed(current_user.uuid)
    return await notifications.get_all_user(current_user.uuid)


@router.get("/system")
async def get_system_banner_notification():
    pass
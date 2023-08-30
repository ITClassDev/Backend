from fastapi import APIRouter, Depends
import uuid as uuid_pkg
from app.notifications.crud import NotificationsCRUD
from app.notifications.schemas import NotificationCreate, NotificationRead, SystemNotificationRead, SystemNotificaionCreate, SystemNotificaionEdit
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
    if current_user:
        data = await notifications.get_active_notifications(current_user.uuid)
        await notifications.set_readed(current_user.uuid)
        return data
    return []

@router.get("/all", response_model=List[NotificationRead])
async def all_my_notifications(notifications: NotificationsCRUD = Depends(get_notifications_crud), current_user: User = Depends(get_current_user)):
    await notifications.set_readed(current_user.uuid)
    return await notifications.get_all_user(current_user.uuid)


@router.get("/system", response_model=List[SystemNotificationRead])
async def get_system_banner_notification(notifications: NotificationsCRUD = Depends(get_notifications_crud)):
    return await notifications.get_system()

@router.get("/system/all", response_model=List[SystemNotificationRead])
async def get_system_banner_notification(notifications: NotificationsCRUD = Depends(get_notifications_crud), _: User = Depends(atleast_teacher_access)):
    return await notifications.get_system(active=False)

@router.put("/system", response_model=SystemNotificationRead)
async def add_system_banner_notification(notification: SystemNotificaionCreate, notifications: NotificationsCRUD = Depends(get_notifications_crud), current_user: User = Depends(atleast_teacher_access)):
    return await notifications.add_system(notification)

@router.patch("/system/{uuid}", response_model=None)
async def edit_system_banner_notification(uuid: uuid_pkg.UUID, notification: SystemNotificaionEdit, notifications: NotificationsCRUD = Depends(get_notifications_crud), current_user: User = Depends(atleast_teacher_access)):
    return await notifications.edit_system(uuid, notification)

@router.delete("/system/{uuid}", response_model=None)
async def delete_system_banner_notification(uuid: uuid_pkg.UUID, notifications: NotificationsCRUD = Depends(get_notifications_crud), current_user: User = Depends(atleast_teacher_access)):
    return await notifications.delete_system(uuid)
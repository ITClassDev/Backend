from fastapi import APIRouter, Depends
from app.notifications.crud import NotificationsCRUD
from app.notifications.schemas import NotificationCreate
from app.notifications.dependencies import get_notifications_crud
from app.auth.dependencies import get_current_user, atleast_teacher_access
from app.users.models import User

router = APIRouter()


@router.put("")
async def send_notification(notification: NotificationCreate, current_user: User = Depends(atleast_teacher_access)):
    pass

@router.get("")
async def notification_polling(notifications: NotificationsCRUD = Depends(get_notifications_crud), current_user: User = Depends(get_current_user)):
    data = await notifications.get_active_notifications(current_user.uuid)
    await notifications.set_readed(current_user.uuid)
    return data

@router.get("/all")
async def all_my_notifications(notifications: NotificationsCRUD = Depends(get_notifications_crud), current_user: User = Depends(get_current_user)):
    return await notifications.get_all_user(current_user.uuid)

@router.get("/system")
async def get_system_banner_notification():
    pass
from fastapi import APIRouter, Depends
from .depends import get_current_user, get_notification_repository, get_user_repository
from repositories.notifications import NotificationRepository
from models.notifications import NotificationToGroup
from repositories.users import UserRepository
from models.user import User

router = APIRouter()

@router.put("/")
async def send_notification(notification: NotificationToGroup, current_user: User = Depends(get_current_user), notifications: NotificationRepository = Depends(get_notification_repository), users: UserRepository = Depends(get_user_repository)):
    if current_user.userRole > 0:
        to_users = await users.get_all_by_group(notification.groupId)
        for user_id in to_users:
            await notifications.send_notification(user_id, notification.type, {"text": notification.text})

@router.get("/polling/")
async def notifications_polling(current_user: User = Depends(get_current_user), notifications: NotificationRepository = Depends(get_notification_repository)):
    data = await notifications.get_active_notifications(current_user.id)
    await notifications.set_readed(current_user.id)
    return data
    

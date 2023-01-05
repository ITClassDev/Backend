from fastapi import APIRouter, Depends
from .depends import get_current_user, get_notification_repository
from repositories.notifications import NotificationRepository
from models.user import User

router = APIRouter()


# @router.get("/set_viewed")
# async def set_viewed(current_user: User = Depends(get_current_user), notifications: NotificationRepository = Depends(get_notification_repository)):
#     await notifications.set_viewed(current_user.id)
#     return {"status": True}
    

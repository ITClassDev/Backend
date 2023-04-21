from fastapi import APIRouter, Depends, HTTPException, status
from repositories.users import UserRepository
from repositories.achievements import AchievementRepository
from repositories.user_groups import UserGroupsRepository
from repositories.notifications import NotificationRepository
from models.user import User, UserUpdate, UserIn
from models.notifications import NotificationToGroup
from .depends import get_user_repository, get_current_user, get_achievement_repository, get_user_groups_repository, get_notification_repository
from core.config import SETUP_MODE, ERROR_TEXTS

router = APIRouter()

@router.get("/moderation_queue/")
async def get_moderation_queue(current_user: User = Depends(get_current_user), achievements: AchievementRepository = Depends(get_achievement_repository)):
    if current_user.userRole > 0:
        return await achievements.get_moderation_queue_for_all()

@router.put("/send_notification/")
async def send_notification(notification: NotificationToGroup, current_user: User = Depends(get_current_user), notifications: NotificationRepository = Depends(get_notification_repository), users: UserRepository = Depends(get_user_repository)):
    if current_user.userRole > 0:
        to_users = await users.get_all_by_group(notification.groupId)
        for user_id in to_users:
            await notifications.send_notification(user_id, notification.type, {"text": notification.text})
#@router.post("/create_admin")
#async def create_admin(new_user_data):
#    pass

if SETUP_MODE:
    @router.put("/setup/")
    async def create_admin(email: str, password: str, users: UserRepository = Depends(get_user_repository), user_groups: UserGroupsRepository = Depends(get_user_groups_repository)):
        if SETUP_MODE:
            group_id = await user_groups.create("Default")
            user_ = UserIn(email=email, firstName="ShTP", lastName="Admin", userRole=2, password=password, learningClass=100, groupId=group_id)
            user_id = await users.create(user_)
            return {"user_id": user_id}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

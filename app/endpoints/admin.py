from fastapi import APIRouter, Depends, HTTPException, status
from repositories.users import UserRepository
from repositories.achievements import AchievementRepository
from repositories.user_groups import UserGroupsRepository
from models.user import User, UserUpdate, UserIn
from .depends import get_user_repository, get_current_user, get_achievement_repository, get_user_groups_repository
from core.config import SETUP_MODE, ERROR_TEXTS

router = APIRouter()

@router.get("/moderation_queue/")
async def get_moderation_queue(current_user: User = Depends(get_current_user), achievements: AchievementRepository = Depends(get_achievement_repository)):
    if current_user.userRole > 0:
        return await achievements.get_moderation_queue_for_all()

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

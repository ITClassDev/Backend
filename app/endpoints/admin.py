from fastapi import APIRouter, Depends
from repositories.users import UserRepository
from repositories.achievements import AchievementRepository
from repositories.user_groups import UserGroupsRepository
from models.user import User, UserUpdate
from .depends import get_user_repository, get_current_user, get_achievement_repository, get_user_groups_repository

router = APIRouter()

LOW_PRIVILEGES_MESSAGE = {"status": False, "detail": "Rejected; Not enough privileges"}

@router.get("/all_users")
async def get_all_users(current_user: User = Depends(get_current_user),
                        users: UserRepository = Depends(get_user_repository), user_groups: UserGroupsRepository = Depends(get_user_groups_repository)):
    if current_user.userRole > 0:  # 1 || 2
        all_users = await users.get_all_users()
        all_user_groups = await user_groups.get_all()
        return {"users": all_users, "user_groups": all_user_groups}
    else:
        return LOW_PRIVILEGES_MESSAGE


@router.patch("/update_user/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate, current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository)):
    if current_user.userRole > 0:  # 1 || 2
        await users.update(user_id, user_data)
        return {"status": True}
    else:
        return LOW_PRIVILEGES_MESSAGE

@router.get("/moderation_queue")
async def get_moderation_queue(current_user: User = Depends(get_current_user), achievements: AchievementRepository = Depends(get_achievement_repository)):
    if current_user.userRole > 0:
        return await achievements.get_moderation_queue_for_all()
from fastapi import APIRouter, Depends
from .depends import get_current_user, get_achievement_repository, get_user_repository
from models.user import User
from models.achievements import AchievementIn
from repositories.achievements import AchievementRepository
from repositories.users import UserRepository

router = APIRouter()

@router.get("/get_my")
async def get_my_achievements(current_user: User = Depends(get_current_user), achievements: AchievementRepository = Depends(get_achievement_repository), users: UserRepository = Depends(get_user_repository)):
    res = {"base": await achievements.get_all_for_user(current_user.id)}
    system = await users.get_user_info(current_user.id)
    res["system"] = system.systemAchievements
    return {"status": True, "achievements": res}

@router.post("/add")
async def add_achievement(achievement: AchievementIn, current_user: User = Depends(get_current_user), achievements: AchievementRepository = Depends(get_achievement_repository)):
    if current_user:
        res = await achievements.add(achievement, current_user.id)
        return {"status": True}

@router.get("/accept/{achievement_id}")
async def accepr_achievement(achievement_id: int, current_user: User = Depends(get_current_user), ):
    pass

@router.get("/my_queue")
async def get_moderation_queue_for_one(current_user: User = Depends(get_current_user), achievements: AchievementRepository = Depends(get_achievement_repository)):
    if current_user:
        return await achievements.get_moderation_queue_for_one(current_user.id)

@router.get("/queu")
async def get_moderation_queue_for_one(current_user: User = Depends(get_current_user), achievements: AchievementRepository = Depends(get_achievement_repository)):
    if current_user.userRole > 0: # for users with status: 1 2 = teachers and super admins
        return await achievements.get_moderation_queue_for_all()
from fastapi import APIRouter, Depends
from .depends import get_current_user, get_achievement_repository
from models.user import User
from repositories.achievements import AchievementRepository

router = APIRouter()

@router.get("/get_my")
async def get_my_achievements(current_user: User = Depends(get_current_user), achievements: AchievementRepository = Depends(get_achievement_repository)):
    res = await achievements.get_all_for_user(current_user.id)
    return {"status": True, "achievements": res}
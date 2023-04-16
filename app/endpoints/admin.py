from fastapi import APIRouter, Depends, HTTPException, status
from repositories.users import UserRepository
from repositories.achievements import AchievementRepository
from models.user import User, UserUpdate, UserIn
from .depends import get_user_repository, get_current_user, get_achievement_repository
from core.config import SETUP_MODE, ERROR_TEXTS

router = APIRouter()


@router.patch("/update_user/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate, current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository)):
    if current_user.userRole > 0:  # 1 || 2
        await users.update(user_id, user_data)
        return {"status": True}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=ERROR_TEXTS.low_permissions)

@router.get("/moderation_queue")
async def get_moderation_queue(current_user: User = Depends(get_current_user), achievements: AchievementRepository = Depends(get_achievement_repository)):
    if current_user.userRole > 0:
        return await achievements.get_moderation_queue_for_all()

#@router.post("/create_admin")
#async def create_admin(new_user_data):
#    pass

if SETUP_MODE:
    @router.put("/setup")
    async def create_admin(email: str, password: str, users: UserRepository = Depends(get_user_repository)):
        if SETUP_MODE:
            user_ = UserIn(email=email, firstName="ShTP", lastName="Admin", userRole=2, password=password, learningClass=100)
            user_id = await users.create(user_)
            return {"user_id": user_id}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

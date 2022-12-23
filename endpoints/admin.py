from fastapi import APIRouter, Depends
from repositories.users import UserRepository
from models.user import User
from .depends import get_user_repository, get_current_user

router = APIRouter()

@router.get("/all_users")
async def get_all_users(current_user: User = Depends(get_current_user), users: UserRepository = Depends(get_user_repository)):
    if current_user.userRole > 0: # 1 || 2
        all_users = await users.get_all_users()
        return all_users
    else:
        return {"status": False, "detail": "Rejected"}
from fastapi import APIRouter, Depends, HTTPException, status
from repositories.users import UserRepository
from models.user import User
from .depends import get_user_repository, get_current_user

router = APIRouter()

@router.get("/{user_id}/info")
async def get_user_info(user_id, users: UserRepository = Depends(get_user_repository)):
    data = await users.get_user_info(int(user_id))
    print(data)
    if data:
        return {"status": True, "first_name": data.first_name, "last_name": data.last_name, "email": data.email, "coins": data.coins, "rating": data.rating, "role": data.user_role}
    return {"status": False, "info": "no user with such id"}

@router.post("/create_user")
async def create_user():
    pass


# Remove on PROD
@router.get("/test_auth")
async def test_auth(current_user: User = Depends(get_current_user)):
    if current_user:
        return {"status": True, "user_id": current_user.id, "user_fname": current_user.first_name}
    else:
        return {"status": False, "info": "Non authed"}
    
from fastapi import APIRouter, Depends, HTTPException, status
from repositories.users import UserRepository
from models.user import User
from .depends import get_user_repository

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


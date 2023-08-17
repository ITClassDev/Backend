from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.users.models import User
router = APIRouter()


@router.get("")
async def get_current_user_achievements(current_user: User = Depends(get_current_user)):
    pass


@router.put("")
async def add_achievements():
    pass


@router.patch("/moderate")
async def accept_achievement():
    pass


@router.get("/pending")
async def get_my_pending_achievements():
    pass


@router.get("/queue")
async def admin_get_all_achievements_queue():
    pass

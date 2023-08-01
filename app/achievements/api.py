from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()


@router.get("")
async def get_my_achievements():
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

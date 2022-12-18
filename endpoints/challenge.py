from fastapi import APIRouter, Depends


router = APIRouter()

@router.get("/get_current")
async def get_current_challenge():
    pass

@router.get("/set_current")
async def get_current_challenge():
    pass

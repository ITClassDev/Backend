from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/my")
async def get_notifications():
    pass

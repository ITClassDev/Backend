from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.get("/{user_id}/info")
async def get_user_info(user_id):
    return {"status": True}

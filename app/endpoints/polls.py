from fastapi import APIRouter, Depends, HTTPException, status
from models.polls import CreatePoll
from models.user import User
from .depends import get_current_user
router = APIRouter()

@router.get("/{poll_id}")
def poll_info(poll_id: int):
    return {"a": 1}

@router.put("/")
def create_poll(poll_data: CreatePoll, current_user: User = Depends(get_current_user)):
    if len(poll_data.entries > 0):
        print(poll_data)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Add atleast one entry to your poll")
from fastapi import APIRouter, Depends, HTTPException, status
from models.polls import PollIn
from models.user import User
from .depends import get_current_user, get_polls_repository
from repositories.polls import PollsRepository
router = APIRouter()

@router.get("/{poll_id}")
async def poll_info(poll_id: int):
    return {"a": 1}

@router.put("/")
async def create_poll(poll_data: PollIn, current_user: User = Depends(get_current_user), polls: PollsRepository = Depends(get_polls_repository)):
    if current_user.userRole in [1, 2]: # If admin
        if len(poll_data.entries) > 0:
            poll_id = await polls.create_poll(poll_data, current_user.id)
            return {"poll_id": poll_id}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Add atleast one entry to your poll")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not enought permissions to execute this API endpoint")
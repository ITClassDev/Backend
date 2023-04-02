from fastapi import APIRouter, Depends, HTTPException, status
from models.polls import PollIn
from models.user import User
from .depends import get_current_user, get_polls_repository
from repositories.polls import PollsRepository

router = APIRouter()

@router.get("/") 
async def get_all(offset: int = 0, limit: int = 50, polls: PollsRepository = Depends(get_polls_repository)):
    return await polls.get_all(offset, limit)

@router.get("/{poll_id}/answers")
async def poll_answers(poll_id: int):
    pass

@router.get("/{poll_id}")
async def poll_info(poll_id: int, polls: PollsRepository = Depends(get_polls_repository)):
    poll = await polls.get_by_id(poll_id)
    if poll:
        return poll
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This poll not found")

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

@router.put("/submit")
async def submit_poll_answer(poll_id: int, poll_data: dict, polls: PollsRepository = Depends(get_polls_repository)): # FIXIT; handle current user for auth_required polls
    # FIXIT check reuired questions answers
    if polls.get_by_id(poll_id):
        answers_id = await polls.submit_answers(poll_id, poll_data)
        return {"answers_id": answers_id}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="We can't find poll with such id")

from fastapi import APIRouter, Depends, HTTPException, status
from models.polls import PollIn
from models.user import User
from .depends import get_current_user, get_polls_repository
from repositories.polls import PollsRepository
import pandas as pd

router = APIRouter()


@router.get("/")
async def get_all(offset: int = 0, limit: int = 50, polls: PollsRepository = Depends(get_polls_repository)):
    return await polls.get_all(offset, limit)


@router.get("/{poll_id}/answers")
async def poll_answers(poll_id: int, offset: int = 0, limit: int = 100, polls: PollsRepository = Depends(get_polls_repository), current_user: User = Depends(get_current_user)):
    if current_user.userRole == 2:  # TODO; only for admins now; FIXIT
        return await polls.get_answers(poll_id, offset, limit)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enought permissions to execute this API endpoint")


@router.get("/{pol_id}/answers/xlsx")
async def poll_answers_xlsx(poll_id: int, polls: PollsRepository = Depends(get_polls_repository), current_user: User = Depends(get_current_user)):
    if current_user.userRole == 2:  # TODO; only for admin now
        poll_questions = [i["text"] for i in dict(await polls.get_by_id(poll_id))["entries"]]
        all_answers_data = await polls.get_answers(poll_id, 0, 100000)
        all_answers = [dict(zip(poll_questions, list(dict(u)["answers"].values())))
                       for u in all_answers_data]  # const max limit
        print(all_answers)
        pd.DataFrame.from_dict(all_answers).to_excel("/tmp/output.xlsx")
        
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enought permissions to execute this API endpoint")


@router.get("/{poll_id}")
async def poll_info(poll_id: int, polls: PollsRepository = Depends(get_polls_repository)):
    poll = await polls.get_by_id(poll_id)
    if poll:
        return poll
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This poll not found")


@router.put("/")
async def create_poll(poll_data: PollIn, current_user: User = Depends(get_current_user), polls: PollsRepository = Depends(get_polls_repository)):
    if current_user.userRole in [1, 2]:  # If admin or teacher
        if len(poll_data.entries) > 0:
            poll_id = await polls.create_poll(poll_data, current_user.id)
            return {"poll_id": poll_id}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Add atleast one entry to your poll")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enought permissions to execute this API endpoint")


@router.put("/{poll_id}/submit/")
# FIXIT; handle current user for auth_required polls
async def submit_poll_answer(poll_id: int, poll_data: dict, polls: PollsRepository = Depends(get_polls_repository)):
    # FIXIT check reuired questions answers; Check trello
    if polls.get_by_id(poll_id):
        answers_id = await polls.submit_answers(poll_id, poll_data)
        return {"answers_id": answers_id}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="We can't find poll with such id")

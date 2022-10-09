from fastapi import APIRouter, Depends
import endpoints.users as users_endpoint
from endpoints.depends import get_user_repository, get_current_user
from core.utils import create_answer
import pbs.main_pb2 as MainBuffer

router = APIRouter()


@router.get("/{user_id}/info", include_in_schema=False)
async def info(user_id: int, users=Depends(get_user_repository)):
    return await create_answer(await users_endpoint.get_user_info(user_id, users), MainBuffer.UserData)

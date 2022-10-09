from fastapi import APIRouter, Depends, Request
import endpoints.auth as auth_endpoint
from endpoints.depends import get_user_repository, get_current_user
from core.utils import create_answer, parse_to_object
import pbs.main_pb2 as MainBuffer
from models.token import Token, Login

router = APIRouter()

@router.post("/login", include_in_schema=False)
async def login(request: Request, users = Depends(get_user_repository)):
    data = await request.body()
    return await create_answer((await auth_endpoint.auth_login(await parse_to_object(data, Login, MainBuffer.AuthData), users)).dict(), MainBuffer.AccessToken)
    


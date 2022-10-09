from fastapi import APIRouter, Depends, HTTPException, status, Request
from models.token import Token, Login
from repositories.users import UserRepository
from core.security import verify_password, create_access_token
from .depends import get_user_repository
from core.utils import check_req_type, create_answer, parse_data
import pbs.main_pb2 as MainBuffer

router = APIRouter()


@router.post("/login", response_model=Token)
async def auth_login(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_user_by_email(login.email)
    if user is None or not verify_password(login.password, user.hashedPassword):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect pair of login && password")
    token = create_access_token({"sub": user.email})
    return Token(accessToken=token, tokenType="Bearer")

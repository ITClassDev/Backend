from fastapi import APIRouter, Depends, HTTPException, status, Request
from models.token import Token, Login
from repositories.users import UserRepository
from core.security import verify_password, create_access_token
from .depends import get_user_repository
from core.utils import check_req_type, create_answer, parse_data
import pbs.main_pb2 as MainBuffer

router = APIRouter()


@router.post("/login")
async def auth_login(request: Request = Request, users: UserRepository = Depends(get_user_repository)):
    req_type = await check_req_type(request)
    if req_type == "application/json":
        req_data = await request.json()
    else:
        req_data = await parse_data(await request.body(), MainBuffer.AuthData)
        req_data = {"email": req_data.email, "password": req_data.password}
    login = Login(
        email=req_data["email"],
        password=req_data["password"]
    )
    user = await users.get_user_by_email(login.email)
    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect pair of login && password")
    token = create_access_token({"sub": user.email})
    if req_type == "application/protobuf":
        token_resp = await create_answer(
            {"access_token": token, "token_type": "Bearer"}, MainBuffer.AccessToken)
    else:
        token_resp = Token(  # Answer for JSON mode
            access_token=token,
            token_type="Bearer"
        )

    return token_resp

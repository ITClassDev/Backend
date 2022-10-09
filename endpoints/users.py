from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, File, UploadFile
from repositories.users import UserRepository
from models.user import User
from .depends import get_user_repository, get_current_user
import pbs.main_pb2 as MainBuffer
from core.utils import create_answer, check_req_type, NON_AUTH_PACKET


router = APIRouter()


@router.get("/{user_id}/info")
async def get_user_info(user_id: int, users: UserRepository = Depends(get_user_repository)):
    #req_type = await check_req_type(request)
    data = await users.get_user_info(int(user_id))
    return_data = {"status": False, "info": "no user with such id"}
    if data:
        return_data = {"status": True, "firstName": data.firstName, "lastName": data.lastName,
                       "email": data.email, "coins": data.coins, "rating": data.rating, "role": data.userRole, "telegramLink": data.userTelegram, "githubLink": data.userGithub, "avatarPath": data.userAvatarPath}
    return return_data


@router.post("/create_user")
async def create_user():
    pass

# Dev route
@router.post("/temp_files")
async def upload_file(request: Request = Request, file: UploadFile = None):
    print(file.filename)

# Remove on PROD


@router.get("/test_auth")
async def test_auth(current_user: User = Depends(get_current_user)):
    if current_user:
        return {"status": True, "userId": current_user.id, "userFname": current_user.first_name}
    return NON_AUTH_PACKET


@router.post("/{user_id}/update_profile")
async def update_user_info(current_user: User = Depends(get_current_user)):
    if current_user:
        print(current_user.id)
    return NON_AUTH_PACKET

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, File, UploadFile
from repositories.users import UserRepository
from models.user import User
from .depends import get_user_repository, get_current_user
import pbs.main_pb2 as MainBuffer
from core.utils import create_answer, check_req_type, NON_AUTH_PACKET, get_file_extension, generate_filename, upload_file


router = APIRouter()


@router.get("/{user_id}/info")
async def get_user_info(user_id: int, users: UserRepository = Depends(get_user_repository)):
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
@router.post("/temp_files_upload")
async def upload_file_test(request: Request = Request, file: UploadFile = None):
    allowed_extensions = ["txt", "png", "jpg"]
    upload_path = "/home/stephan/Progs/ItClassBackend/static/users_data/uploads"
    return await upload_file(file, allowed_extensions, upload_path)


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

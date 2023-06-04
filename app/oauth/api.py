from fastapi import APIRouter
import uuid as uuid_pkg

router = APIRouter()


@router.get("")
async def get_app_info():
    pass


@router.put("")
async def create_app():
    pass


@router.post("/provide_access")
async def provide_access_to_api():
    pass


@router.get("/get_user/{user_uuid}")
async def get_app_info(user_uuid: uuid_pkg.UUID):
    return user_uuid

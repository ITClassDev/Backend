from fastapi import APIRouter, Depends
from repositories.apps import AppsRepository
from .depends import get_apps_repository, get_current_user
from models.apps import ProvideAccessRequest
from models.user import User
from core.security import create_oauth_access_token
import requests

router = APIRouter()

@router.get("/get_app/:app_id")
async def get_app_info(app_id: int, apps: AppsRepository = Depends(get_apps_repository)):
    data = await apps.get_by_id(app_id)
    return data

@router.post("/provide_access") # generate temp token to access some user endpoints with another prefix
async def provide_access(app_info: ProvideAccessRequest, current_user: User = Depends(get_current_user)):
    if current_user:
        access_token = create_oauth_access_token(to_user)
        return {"status": True, "info": "Access provided"}
    else:
        return {"status": False}
from fastapi import APIRouter, Depends
from repositories.apps import AppsRepository
from .depends import get_apps_repository

router = APIRouter()

@router.get("/get_app/:app_id")
async def get_app_info(app_id: int, apps: AppsRepository = Depends(get_apps_repository)):
    data = await apps.get_by_id(app_id)
    return data
from fastapi import APIRouter


router = APIRouter()


@router.put("")
async def send_notification():
    pass


@router.get("")
async def notification_polling():
    pass

@router.get("all")
async def all_my_notifications():
    pass
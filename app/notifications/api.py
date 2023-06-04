from fastapi import APIRouter


router = APIRouter()


@router.put("")
async def send_notification():
    pass


@router.get("")
async def notification_polling():
    pass
from pydantic import BaseModel
import uuid as uuid_pkg
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    toUser: Optional[uuid_pkg.UUID] = None
    toGroup: Optional[uuid_pkg.UUID] = None
    type: int
    data: dict

    class Config:
        schema_extra = {"example": {
            "toUser": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "toGroup": "1ca15f31-5717-4562-b3fc-2c963f66afa6",
            "type": 0,
            "data": {"name": "Финалист НТО", "points": 100}
        }}
class NotificationRead(BaseModel):
    uuid: uuid_pkg.UUID
    toUser: uuid_pkg.UUID
    type: int
    data: dict
    viewed: bool
    created_at: datetime


class SystemNotificationRead(BaseModel):
    uuid: uuid_pkg.UUID
    type: str
    active: bool
    title: str
    content: str

class SystemNotificaionCreate(BaseModel):
    type: str
    active: bool
    title: str
    content: str

class SystemNotificaionEdit(BaseModel):
    type: Optional[str] = None
    active: Optional[bool] = None
    title: Optional[str] = None
    content: Optional[str] = None
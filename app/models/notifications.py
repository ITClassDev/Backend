from pydantic import BaseModel
from typing import Optional

class Notification(BaseModel):
    id: Optional[int] = None
    to_user: int
    type: int
    viewed: bool
    data: dict

class NotificationToGroup(BaseModel):
    groupId: int
    text: str
    type: int

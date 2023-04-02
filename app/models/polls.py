from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Poll(BaseModel):
    id: Optional[int] = None
    owner_id: int
    title: str
    description: str
    auth_required: Optional[bool] = False
    entries: List[dict]
    created_at: datetime
    expire_at: Optional[datetime] = None

class PollIn(BaseModel):
    title: str
    description: str
    auth_required: Optional[bool] = False
    entries: List[dict]
    expire_at: Optional[datetime] = None

class PollAnswer(BaseModel):
    id: Optional[int] = None
    poll_id: int
    user_id: Optional[int] = None
    answers: dict


# class PollEntry(BaseModel):
#     id: Optional[int] = None
#     title: str
#     description: Optional[str] = None
#     image_path: Optional[str] = None
#     entry_type: int
#     checkboxes_variants: Optional[dict] = None
#     select_variants: Optional[dict] = None


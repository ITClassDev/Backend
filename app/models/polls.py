from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Poll(BaseModel):
    id: Optional[int] = None
    owner_id: int
    title: str
    description: str
    auth_required: bool
    entries: List[dict]
    created_at: datetime
    expire_at: datetime

class PollIn(BaseModel):
    title: str
    description: str
    auth_required: bool
    entries: List[dict]
    expire_at: datetime

# class PollEntry(BaseModel):
#     id: Optional[int] = None
#     title: str
#     description: Optional[str] = None
#     image_path: Optional[str] = None
#     entry_type: int
#     checkboxes_variants: Optional[dict] = None
#     select_variants: Optional[dict] = None


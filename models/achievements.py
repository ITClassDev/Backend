from pydantic import BaseModel
from typing import Optional
import datetime

class Achievement(BaseModel):
    id: Optional[int] = None
    to_user: int
    accepted_by: Optional[int] = None
    type: int
    title: str
    description: str
    points: int
    received_at: datetime.datetime

class AchievementIn(BaseModel):
    type: int
    title: str
    description: str
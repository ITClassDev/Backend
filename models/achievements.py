from pydantic import BaseModel
from typing import Optional
import datetime

class Achievement(BaseModel):
    id: Optional[int] = None
    to_user: int
    accepted_by: int
    type: int
    title: str
    description: str
    point: int
    received_at: datetime.datetime


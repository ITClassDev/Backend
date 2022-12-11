from pydantic import BaseModel
from typing import Optional
import datetime

class App(BaseModel):
    id: Optional[int] = None
    owner_id: id
    name: str
    permission_level: int
    verified: bool
    created_at: datetime.datetime

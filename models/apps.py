from pydantic import BaseModel
from typing import Optional
import datetime

class App(BaseModel):
    id: Optional[int] = None
    owner_id: id
    name: str
    permission_level: int
    verified: bool
    redirect_url: str
    created_at: datetime.datetime

class ProvideAccessRequest(BaseModel):
    app_id: int
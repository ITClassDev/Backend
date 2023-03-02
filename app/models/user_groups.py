from pydantic import BaseModel
from typing import Optional

class UserGroup(BaseModel):
    id: Optional[int] = None
    name: str
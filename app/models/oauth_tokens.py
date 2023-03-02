from pydantic import BaseModel
from typing import Optional

class OauthToken(BaseModel):
    entry_id: Optional[int] = None
    token: str
    app_id: int
    to_user: int
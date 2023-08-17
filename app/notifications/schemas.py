from pydantic import BaseModel
import uuid as uuid_pkg
from typing import Optional

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

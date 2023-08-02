from pydantic import BaseModel
import uuid as uuid_pkg

class NotificationCreate(BaseModel):
    toUser: uuid_pkg.UUID
    type: int
    viewed: bool
    data: dict

    class Config:
        schema_extra = {"example": {
            "toUser": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "type": 0,
            "viewed": False,
            "data": {"name": "Финалист НТО", "points": 100}
        }}
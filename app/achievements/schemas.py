from pydantic import BaseModel
from app.users.schemas import MinimalUser
import json
import uuid as uuid_pkg
import datetime
from typing import Optional

class AchievementCreate(BaseModel):
    eventType: str
    title: str
    description: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    

    class Config:
        schema_extra = {"example": {
            "eventType": "olimpiad or event",
            "title": "Моё достижение",
            "description": "Описание достижения"
        }}


class AchievementRead(BaseModel):
    uuid: uuid_pkg.UUID
    eventType: str
    title: str
    description: str
    attachmentName: str
    created_at: datetime.datetime
    

    points: Optional[int] = None
    acceptedAt: Optional[datetime.datetime] = None
    acceptedBy: Optional[uuid_pkg.UUID] = None
    

    User: MinimalUser


class AchievementModerate(BaseModel):
    uuid: uuid_pkg.UUID
    status: int
    points: Optional[int] = None
    class Config:
        schema_extra = {"example": {
            "uuid": "Achievement UUID",
            "status": "0 - reject | 1 - accept",
            "points": 100
        }}

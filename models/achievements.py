from pydantic import BaseModel
from typing import Optional
import datetime
import json

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
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AchievementModerate(BaseModel):
    id: int
    status: int
    points: Optional[int] = 0
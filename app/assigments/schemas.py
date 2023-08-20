from pydantic import BaseModel
from typing import List, Optional
import uuid as uuid_pkg
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    text: str
    timeLimit: int
    memoryLimit: int
    dayChallenge: bool
    tests: Optional[List[dict]] = None
    testsTypes: Optional[dict] = None
    functionName: Optional[str] = None

    class Config:
        schema_extra = {"example": {
            "title": "Task title",
            "text": "Task full text - description",
            "timeLimit": 1,
            "memoryLimit": 512,
            "dayChallenge": False,
            "tests": [{"input": "1 2", "output": "3"}],
            "testsTypes": [{"input": ["string", "string"], "output": ["string"]}],
            "functionName": "testForContestName"
        }}


class TaskSearch(BaseModel):
    uuid: uuid_pkg.UUID
    title: str


class TaskLeaderBoard(BaseModel):
    userId: uuid_pkg.UUID
    firstName: str
    lastName: str
    avatarPath: str
    nickName: Optional[str] = None
    created_at: datetime


class ContestCreate(BaseModel):
    tasks: List[uuid_pkg.UUID]
    forGroups: List[uuid_pkg.UUID]
    title: str
    description: str
    deadline: Optional[datetime] = None
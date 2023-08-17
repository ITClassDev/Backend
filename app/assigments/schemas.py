from pydantic import BaseModel
from typing import List

class TaskCreate(BaseModel):
    title: str
    text: str
    timeLimit: int
    memoryLimit: int
    dayChallenge: bool
    tests: List[dict]
    testsTypes: List[dict]
    functionName: str

    class Config:
        schema_extra = {"example": {
            "title": "Task title",
            "text": "Task full text - description",
            "timeLimit": 1,
            "memoryLimit": 512,
            "dayChallenge": False,
            "tests": [{}],
            "testsTypes": [{}],
            "functionName": "get_abbb"
        }}
    
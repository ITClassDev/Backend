from pydantic import BaseModel
from typing import List, Optional
import uuid as uuid_pkg
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    text: str
    timeLimit: int
    memoryLimit: int
    dayChallenge: Optional[bool] = False
    tests: List[dict]
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
    submitId: uuid_pkg.UUID
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
    forLearningClass: int

class ContestSubmitGithub(BaseModel):
    contest: uuid_pkg.UUID
    githubLink: str
    language: str
    class Config:
        schema_extra = {"example": {
            "contest": uuid_pkg.uuid4(),
            "githubLink": "https://github.com/ItClassDev/TestSolutions",
            "language": "cpp OR py"
        }}

class SubmitSourceCode(BaseModel):
    language: str
    source: str

class ContestsSolvedTasks(BaseModel):
    solved: List[uuid_pkg.UUID]
    failed: List[uuid_pkg.UUID]

class ContestRead(BaseModel):
    uuid: uuid_pkg.UUID
    created_at: datetime
    updated_at: datetime
    authorId: uuid_pkg.UUID
    title: str
    description: str
    deadline: datetime
    tasks: List[uuid_pkg.UUID]
    forGroups: List[uuid_pkg.UUID]
    forLearningClass: Optional[int]
    solvedPercentage: Optional[float]


class ContestStatisticsSolved(BaseModel):
    userId: uuid_pkg.UUID
    firstName: str
    lastName: str
    solvedCount: int
    nickName: Optional[str]
    avatarPath: str

class ContestStatistics(BaseModel):
    tasksCount: int
    students: List[ContestStatisticsSolved]
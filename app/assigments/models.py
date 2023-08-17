import uuid as uuid_pkg
from sqlalchemy import Column, JSON, String
from sqlalchemy.types import ARRAY
from app.core.models import TimestampModel, UUIDModel
from sqlmodel import Field
from typing import List

class Task(UUIDModel, TimestampModel, table=True):
    __tablename__ = "tasks"
    authorId: uuid_pkg.UUID = Field(foreign_key="users.uuid", nullable=False)
    title: str = Field(nullable=False)
    text: str = Field(nullable=False)
    timeLimit: int = Field(nullable=False, default=1)
    memoryLimit: int = Field(nullable=False, default=512)
    dayChallenge: bool = Field(nullable=False, default=False)
    tests: List[dict] = Field(sa_column=Column(
        "tests",
        JSON
    ), nullable=True)
    testsTypes: List[dict] = Field(sa_column=Column(
        "types",
        JSON
    ), nullable=True)
    functionName: str = Field(nullable=True)


class Contest(UUIDModel, TimestampModel, table=True):
    __tablename__ = "contests"
    authorId: uuid_pkg.UUID = Field(foreign_key="users.uuid", nullable=False)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    tasks: List[uuid_pkg.UUID] = Field(sa_column=Column(
        "tasks",
        ARRAY(String)
    ))
    forGroups: List[uuid_pkg.UUID] = Field(sa_column=Column(
        "forGroups",
        ARRAY(String)
    ))
    # TODO; Add special users list

class Submit(UUIDModel, TimestampModel, table=True):
    __tablename__ = "submits"
    userId: uuid_pkg.UUID = Field(foreign_key="users.uuid", nullable=False)
    status: int = Field(nullable=False)
    taskId: uuid_pkg.UUID = Field(foreign_key="tasks.uuid", nullable=False)
    source: str = Field(nullable=False)
    referedContest: uuid_pkg.UUID = Field(nullable=True) # If submit contest
    gitCommitId: str = Field(nullable=True) # If submit contest
    solved: bool = Field(nullable=False, default=False)
    testsResults: dict = Field(sa_column=Column(
        "testsResults",
        JSON
    ), nullable=True)
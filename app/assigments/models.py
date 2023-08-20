import uuid as uuid_pkg
from sqlalchemy import Column, JSON, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.core.models import TimestampModel, UUIDModel
from sqlmodel import Field, Relationship
from typing import List, Optional
from datetime import datetime

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
    testsTypes: Optional[dict] = Field(sa_column=Column(
        "types",
        JSON
    ), nullable=True)
    functionName: Optional[str] = Field(nullable=True)


class Contest(UUIDModel, TimestampModel, table=True):
    __tablename__ = "contests"
    authorId: uuid_pkg.UUID = Field(foreign_key="users.uuid", nullable=False)
    title: str = Field(nullable=False)
    description: str = Field(nullable=False)
    deadline: datetime = Field(nullable=True, default=None)
    
    tasks: List[uuid_pkg.UUID] = Field(sa_column=Column(
        "tasks",
        ARRAY(UUID(as_uuid=1))
    ))
    forGroups: List[uuid_pkg.UUID] = Field(sa_column=Column(
        "forGroups",
        ARRAY(UUID(as_uuid=1))
    ))
    forLearningClass: int = Field(nullable=True)
    # TODO; Add special users list

class Submit(UUIDModel, TimestampModel, table=True):
    __tablename__ = "submits"
    userId: uuid_pkg.UUID = Field(
        nullable=False,
        sa_column=Column(UUID(as_uuid=1), ForeignKey("users.uuid", ondelete="CASCADE")) 
    )
    user: Optional["User"] = Relationship(back_populates="submits")

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
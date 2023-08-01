from sqlalchemy import Column, event, table
from sqlalchemy.databases import postgres
from sqlmodel import Field, SQLModel
import uuid as uuid_pkg

from app.core.models import TimestampModel, UUIDModel

users_role_type = postgres.ENUM(
    "student",
    "teacher",
    "admin",
    name=f"user_role"
)


@event.listens_for(SQLModel.metadata, "before_create")
def _create_enums(metadata, conn, **kw):
    users_role_type.create(conn, checkfirst=True)


class User(UUIDModel, TimestampModel, table=True):
    __tablename__ = "users"  # type: ignore
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    role: str = Field(sa_column=Column(
        "role",
        users_role_type,
        nullable=False,
        default="student"
    ))
    rating: int = Field(default=0, nullable=False)
    learningClass: int = Field(default=0, nullable=False)
    groupId: uuid_pkg.UUID = Field(nullable=False, foreign_key="groups.uuid")
    shtpMaintainer: bool = Field(default=0, nullable=True)
    nickName: str = Field(max_length=100, nullable=True, unique=True)
    firstName: str = Field(max_length=50, nullable=False)
    lastName: str = Field(max_length=50, nullable=False)
    aboutText: str = Field(max_length=100, nullable=True)
    patronymicName: str = Field(max_length=50, nullable=True)
    avatarPath: str = Field(nullable=False, default="default.png")

    telegram: str = Field(max_length=100, nullable=True, unique=True)
    github: str = Field(max_length=100, nullable=True, unique=True)
    stepik: str = Field(max_length=100, nullable=True, unique=True)
    kaggle: str = Field(max_length=100, nullable=True, unique=True)
    website: str = Field(max_length=100, nullable=True, unique=True)

    techStack: str = Field(max_length=800, nullable=True)



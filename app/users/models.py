from typing import Optional
import uuid as uuid_pkg
from sqlalchemy import Column, event, table
from sqlalchemy.databases import postgres
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, EmailStr, root_validator

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
    groupId: int = Field(nullable=False)
    shtpMaintainer: bool = Field(default=0, nullable=True)
    nickName: str = Field(max_length=100, nullable=True, unique=True)
    firstName: str = Field(max_length=50, nullable=False)
    lastName: str = Field(max_length=50, nullable=False)
    patronymicName: str = Field(max_length=50, nullable=True)
    avatarPath: str = Field(nullable=False, default="default.png")

    telegram: str = Field(max_length=100, nullable=True, unique=True)
    github: str = Field(max_length=100, nullable=True, unique=True)
    stepik: str = Field(max_length=100, nullable=True, unique=True)
    kaggle: str = Field(max_length=100, nullable=True, unique=True)
    website: str = Field(max_length=100, nullable=True, unique=True)

    techStack: str = Field(max_length=800, nullable=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    role: str
    groupId: int

    class Config:
        schema_extra = {"example": {
            "email": "email@yandex.ru",
            "password": "12345",
            "firstname": "Ivan",
            "lastname": "Ivanov"
        }}


class UserRead(BaseModel):
    uuid: uuid_pkg.UUID
    role: str
    nickname: str
    email: str
    firstname: str
    lastname: str
    avatar: str
    showcontacts: bool
    github: Optional[str]
    telegram: Optional[str]
    tel: Optional[str]

    @root_validator
    def hide_contacts(cls, values):
        if not values["showcontacts"]:
            values["github"] = "Hidden"
            values["telegram"] = "Hidden"
            values["tel"] = "Hidden"
            values["email"] = "Hidden"
        return values


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {"example": {
            "email": "email@yandex.ru",
            "password": "12345"
        }}

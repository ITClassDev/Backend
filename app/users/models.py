from typing import Optional, List
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
    aboutText: str = Field(max_length=100, nullable=True)
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
    learningClass: int

    class Config:
        schema_extra = {"example": {
            "email": "email@1561.ru",
            "password": "12345",
            "firstName": "Ivan",
            "lastName": "Ivanov",
            "role": "student",
            "learningClass": 10,
            "groupId": 1
        }}


class UserRead(BaseModel):
    uuid: uuid_pkg.UUID
    role: str
    rating: int
    learningClass: int
    shtpMaintainer: bool
    groupId: int
    nickName: Optional[str]
    firstName: str
    lastName: str
    patronymicName: Optional[str]
    avatarPath: str
    telegram: Optional[str]
    github: Optional[str]
    stepik: Optional[str]
    kaggle: Optional[str]
    website: Optional[str]
    techStack: Optional[str]


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {"example": {
            "email": "email@1561.ru",
            "password": "12345"
        }}


class SocialLinks(BaseModel):
    github: Optional[str]
    telegram: Optional[str]
    stepik: Optional[str]
    kaggle: Optional[str]
    website: Optional[str]


class UpdatePassword(BaseModel):
    currentPassword: str
    newPassword: str
    confirmPassword: str


class UserUpdateAdmin(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    patronymicName: Optional[str]
    rating: Optional[int]
    learningClass: Optional[int]


class UserUpdate(BaseModel):
    uuid: Optional[uuid_pkg.UUID] = None
    aboutText: Optional[str] = None
    nickName: Optional[str] = None
    socialLinks: Optional[SocialLinks]
    techStack: Optional[List[str]]
    password: Optional[UpdatePassword]
    admin: Optional[UserUpdateAdmin]

    class Config:
        schma_extra = {"example": {
            "uuid": "If you are admin/teacher and want to modify another user data",
            "aboutText": "string",
            "nickName": "string",
            "socialLinks": {
                "github": "string",
                "telegram": "string",
                "stepik": "string",
                "kaggle": "string",
                "website": "string"
            },
            "techStack": [
                "string"
            ],
            "password": {
                "currentPassword": "string",
                "newPassword": "string",
                "confirmPassword": "string"
            },
            "admin": {
                "firstName": "string",
                "lastName": "string",
                "patronymicName": "string",
                "rating": 0,
                "learningClass": 0
            }
        }}

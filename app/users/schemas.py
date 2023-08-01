from typing import Optional
import uuid as uuid_pkg
from pydantic import BaseModel, EmailStr
from typing import List


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    role: str
    groupId: uuid_pkg.UUID
    learningClass: int

    class Config:
        schema_extra = {"example": {
            "email": "email@1561.ru",
            "password": "12345",
            "firstName": "Ivan",
            "lastName": "Ivanov",
            "role": "student",
            "learningClass": 10,
            "groupId": ""
        }}


class UserRead(BaseModel):
    uuid: uuid_pkg.UUID
    role: str
    rating: int
    learningClass: int
    shtpMaintainer: Optional[bool] = False
    groupId: uuid_pkg.UUID
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
    aboutText: Optional[str] = None


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

class UserUpdateResponse(BaseModel):
    # Any user can update for self account
    aboutText: Optional[str] = None
    nickName: Optional[str] = None
    github: Optional[str] = None
    telegram: Optional[str] = None
    stepik: Optional[str] = None
    kaggle: Optional[str] = None
    website: Optional[str] = None
    techStack: Optional[str] = None
    password: Optional[str] = None

    # Only admin can update
    password: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    patronymicName: Optional[str] = None
    rating: Optional[int] = None
    learningClass: Optional[int] = None

    


class UpdateAvatarResponse(BaseModel):
    avatar: str


class LeaderboardUser(BaseModel):
    uuid: uuid_pkg.UUID
    nickName: Optional[str] = ""
    firstName: str
    lastName: str
    avatarPath: str
    rating: int

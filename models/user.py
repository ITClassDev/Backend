from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    hashedPassword: str
    firstName: str
    lastName: str
    middleName: Optional[str]
    rating: int
    userRole: int
    learningClass: int
    userTelegram: Optional[str]
    userGithub: Optional[str]
    userStepik: Optional[str]
    userKaggle: Optional[str]
    userAboutText: str
    userAvatarPath: str


class UserIn(BaseModel):
    email: EmailStr
    hashedPassword: str
    firstName: str
    lastName: str
    rating: int
    userRole: int
    learningClass: int


class AboutText(BaseModel):
    about_text: str

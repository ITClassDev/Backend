from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    hashedPassword: str
    firstName: str
    lastName: str
    middleName: Optional[str]
    rating: Optional[int]
    userRole: int
    learningClass: int
    userTelegram: Optional[str]
    userGithub: Optional[str]
    userStepik: Optional[str]
    userKaggle: Optional[str]
    userWebsite: Optional[str]
    userAboutText: Optional[str]
    userAvatarPath: Optional[str]
    systemAchievements: Optional[List]
    techStack: Optional[str] = None
    groupId: int

    # @validator('techStack')
    # def set_name(cls, name):
    #     return name or ""



class UserIn(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    userRole: int
    password: str
    learningClass: int
    groupId: int


class UserUpdate(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    rating: int
    userRole: int
    learningClass: int
    userAboutText: str


class AboutText(BaseModel):
    about_text: str


class SocialLinksIn(BaseModel):
    github: Optional[str]
    telegram: Optional[str]
    stepik: Optional[str]
    kaggle: Optional[str]
    website: Optional[str]

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class UpdateTechStack(BaseModel):
    tech_stack: list
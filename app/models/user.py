from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    hashedPassword: str
    firstName: str
    lastName: str
    middleName: Optional[str]
    rating: Optional[int] = 0
    userRole: int
    learningClass: int
    userTelegram: Optional[str]
    userGithub: Optional[str]
    userStepik: Optional[str]
    userKaggle: Optional[str]
    userWebsite: Optional[str]
    userAboutText: Optional[str]
    userAvatarPath: Optional[str] = "default.png"
    systemAchievements: Optional[List]
    techStack: Optional[str] = None
    groupId: Optional[int] = None

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
    groupId: Optional[int] = None


class SocialLinks(BaseModel):
    userGithub: Optional[str]
    userTelegram: Optional[str]
    userStepik: Optional[str]
    userKaggle: Optional[str]
    userWebsite: Optional[str]


class UpdatePassword(BaseModel):
    currentPassword: str
    newPassword: str
    confirmPassword: str

class UserUpdateAdmin(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    middleName: Optional[str]
    rating: Optional[int]
    learningClass: Optional[int]

class UserUpdate(BaseModel):
    aboutText: Optional[str]
    socialLinks: Optional[SocialLinks]
    techStack: Optional[List[str]]
    password: Optional[UpdatePassword]
    admin: Optional[UserUpdateAdmin]

class AboutText(BaseModel):
    about_text: str


class SocialLinksIn(BaseModel):
    github: Optional[str]
    telegram: Optional[str]
    stepik: Optional[str]
    kaggle: Optional[str]
    website: Optional[str]
class UpdateTechStack(BaseModel):
    tech_stack: list

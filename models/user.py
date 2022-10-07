from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    hashedPassword: str
    firstName: str
    lastName: str
    coins: int
    rating: int
    userRole: int
    userTelegram: str
    userGithub: str
    userAboutText: str
    userAvatarPath: str

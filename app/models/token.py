from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    accessToken: str
    tokenType: str

class Login(BaseModel):
    email: EmailStr
    password: str

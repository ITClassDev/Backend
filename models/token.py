from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    accessToken: str
    tokenType: str

class Login(BaseModel):
    email: EmailStr
    password: str

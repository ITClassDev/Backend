from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    coins: int
    rating: int
    user_role: int

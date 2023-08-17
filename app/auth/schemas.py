from pydantic import BaseModel

class AuthData(BaseModel):
    accessToken: str
    refreshToken: str

class NewAccessToken(BaseModel):
    accessToken: str
    
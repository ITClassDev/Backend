import datetime
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from jose import jwt
import string
import random
import jose
from .config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash_: str) -> bool:
    return pwd_context.verify(password, hash_)


def create_oauth_access_token(to_user: int, app_id: int) -> str:
    payload_avaliable = string.ascii_letters + "()-_*!<>"
    return f"oauth_access_{(to_user * app_id) * random.randint(3, 20)}_{''.join(random.choice(payload_avaliable) for x in range(14))}"

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() +
                     datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    try:
        encoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWSError:
        return None
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        try:
            credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
            exp = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")
            if credentials:
                token = decode_access_token(credentials.credentials)
                if token is None:
                    raise exp
                return credentials.credentials
            else:
                raise exp
        except (jose.exceptions.ExpiredSignatureError, jose.exceptions.JWTError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Credentials invalid")

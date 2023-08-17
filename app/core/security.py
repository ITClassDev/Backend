from passlib.context import CryptContext
import passlib

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    try:
        return password_context.verify(password, hashed_pass)
    except passlib.exc.UnknownHashError: # Invalid hash signature
        return False

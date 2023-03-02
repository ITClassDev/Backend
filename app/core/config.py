from starlette.config import Config

config = Config(".env")
DATABASE_URL = config("ITC_DATABASE_URL", cast=str, default="")
SERVER_HOST = config("ITC_SERV_HOST", cast=str, default="0.0.0.0")
SERVER_PORT = config("ITC_SERV_PORT", cast=int, default=8080)
ACCESS_TOKEN_EXPIRE_MINUTES = config("ITC_ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=120) # Session time in minutes
ALGORITHM = "HS256"
SECRET_KEY = config("ITC_SECRET_KEY", cast=str, default="212646234g2634234f23642fc46234c2634")
USERS_STORAGE = config("ITC_USERS_STORAGE", cast=str)
API_VER = config("ITC_API_VER", cast=str)

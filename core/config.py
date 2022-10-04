from starlette.config import Config

config = Config(".env")
DATABASE_URL = config("ITC_DATABASE_URL", cast=str, default="")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Session time
ALGORITHM = "HS256"
SECRET_KEY = config("ITC_SECRET_KEY", cast=str, default="212646234g2634234f23642fc46234c2634")


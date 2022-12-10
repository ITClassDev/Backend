from .users import users
from .achievements import achievements
from .base import metadata, engine

metadata.create_all(bind=engine)
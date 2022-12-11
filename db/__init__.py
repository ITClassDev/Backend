from .users import users
from .achievements import achievements
from .apps import apps
from .base import metadata, engine

metadata.create_all(bind=engine)
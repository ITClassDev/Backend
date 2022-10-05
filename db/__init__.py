from .users import users
from .base import metadata, engine

metadata.create_all(bind=engine)

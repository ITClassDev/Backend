from .users import users
from .achievements import achievements
from .apps import apps
from .oauth_tokens import oauth_tokens
from .base import metadata, engine

metadata.create_all(bind=engine)
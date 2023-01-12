from .users import users
from .achievements import achievements
from .apps import apps
from .oauth_tokens import oauth_tokens
from .notifications import notifications
from .user_groups import user_groups
from .tasks import tasks
from .base import metadata, engine

metadata.create_all(bind=engine)
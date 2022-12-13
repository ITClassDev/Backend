import sqlalchemy
from .base import engine, metadata

oauth_tokens = sqlalchemy.Table(
    "oauth_tokens",
    metadata,
    sqlalchemy.Column("entry_id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("token", sqlalchemy.String),
    sqlalchemy.Column("app_id", sqlalchemy.Integer),
    sqlalchemy.Column("to_user", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
)
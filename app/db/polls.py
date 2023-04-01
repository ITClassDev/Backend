import sqlalchemy
from .base import engine, metadata

polls = sqlalchemy.Table(
    "polls",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("owner_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("auth_required", sqlalchemy.Boolean),
    sqlalchemy.Column("entries", sqlalchemy.PickleType),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("expire_at", sqlalchemy.DateTime),
)
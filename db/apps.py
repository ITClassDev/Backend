import sqlalchemy
from .base import engine, metadata

apps = sqlalchemy.Table(
    "thirdparty_apps",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("owner_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("permission_level", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("verified", sqlalchemy.Boolean)
)
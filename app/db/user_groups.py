import sqlalchemy
from .base import metadata

user_groups = sqlalchemy.Table(
    "user_groups",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,
                      primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String),
)

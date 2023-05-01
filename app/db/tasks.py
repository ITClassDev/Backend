import sqlalchemy
from .base import engine, metadata

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("author_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("time_limit", sqlalchemy.Integer, default=1),
    sqlalchemy.Column("memory_limit", sqlalchemy.Integer, default=512),
    sqlalchemy.Column("is_day_challenge", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("tests", sqlalchemy.PickleType),
    sqlalchemy.Column("types", sqlalchemy.PickleType),
    sqlalchemy.Column("func_name", sqlalchemy.String),
)
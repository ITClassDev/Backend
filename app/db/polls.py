import sqlalchemy
from .base import engine, metadata

polls = sqlalchemy.Table(
    "polls",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("owner_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("auth_required", sqlalchemy.Boolean),
    sqlalchemy.Column("entries", sqlalchemy.PickleType),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("expire_at", sqlalchemy.DateTime),
)

polls_answers = sqlalchemy.Table(
    "polls_answers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True),
    sqlalchemy.Column("poll_id", sqlalchemy.Integer),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=True),
    sqlalchemy.Column("answers", sqlalchemy.PickleType),
    sqlalchemy.Column("answer_date", sqlalchemy.DateTime),
)
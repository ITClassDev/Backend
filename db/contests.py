import sqlalchemy
from .base import engine, metadata

contests = sqlalchemy.Table(
    "contests",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("author_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("tasks_ids_list", sqlalchemy.types.ARRAY(sqlalchemy.Integer)),
    sqlalchemy.Column("users_ids_tags", sqlalchemy.types.ARRAY(sqlalchemy.Integer)),
)
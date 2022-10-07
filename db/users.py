import sqlalchemy
from .base import metadata, engine
import datetime

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,
                      primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String,
                      primary_key=True, unique=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("coins", sqlalchemy.Integer),
    sqlalchemy.Column("rating", sqlalchemy.Integer),
    sqlalchemy.Column("user_role", sqlalchemy.Integer,
                      default=0),  # Default non admin user
    sqlalchemy.Column("user_telegram", sqlalchemy.String),
    sqlalchemy.Column("user_github", sqlalchemy.String),
    sqlalchemy.Column("user_about_text", sqlalchemy.String),
    sqlalchemy.Column("user_avatar_path", sqlalchemy.String),



)

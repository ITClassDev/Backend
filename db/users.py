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
    sqlalchemy.Column("hashedPassword", sqlalchemy.String),
    sqlalchemy.Column("firstName", sqlalchemy.String),
    sqlalchemy.Column("lastName", sqlalchemy.String),
    sqlalchemy.Column("coins", sqlalchemy.Integer),
    sqlalchemy.Column("rating", sqlalchemy.Integer),
    sqlalchemy.Column("userRole", sqlalchemy.Integer,
                      default=0),  # Default non admin user
    sqlalchemy.Column("userTelegram", sqlalchemy.String),
    sqlalchemy.Column("userGithub", sqlalchemy.String),
    sqlalchemy.Column("userAboutText", sqlalchemy.String),
    sqlalchemy.Column("userAvatarPath", sqlalchemy.String),



)

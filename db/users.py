import sqlalchemy
from .base import metadata
from sqlalchemy.types import ARRAY

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
    sqlalchemy.Column("middleName", sqlalchemy.String),
    sqlalchemy.Column("rating", sqlalchemy.Integer),
    sqlalchemy.Column("userRole", sqlalchemy.Integer,
                      default=0),  # Default non admin user
    sqlalchemy.Column("learningClass", sqlalchemy.Integer),
    sqlalchemy.Column("userTelegram", sqlalchemy.String),
    sqlalchemy.Column("userGithub", sqlalchemy.String),
    sqlalchemy.Column("userStepik", sqlalchemy.String),
    sqlalchemy.Column("userKaggle", sqlalchemy.String),
    sqlalchemy.Column("userAboutText", sqlalchemy.String),
    sqlalchemy.Column("userAvatarPath", sqlalchemy.String,
                      default="default.png"),
    sqlalchemy.Column("systemAchievements", ARRAY(sqlalchemy.Integer)),
    sqlalchemy.Column("techStack", sqlalchemy.String)
)

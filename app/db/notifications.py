import sqlalchemy
from .base import metadata

notifications = sqlalchemy.Table(
    "notifications",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("to_user", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column("type", sqlalchemy.Integer),
    sqlalchemy.Column("viewed", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("data", sqlalchemy.PickleType),
)
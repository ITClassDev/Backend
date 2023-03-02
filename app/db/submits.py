import sqlalchemy
from .base import engine, metadata

submits = sqlalchemy.Table(
    "submits",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.Integer),
    sqlalchemy.Column("task_id", sqlalchemy.Integer),
    sqlalchemy.Column("source", sqlalchemy.String),
    sqlalchemy.Column("refer_to", sqlalchemy.Integer), # contest id Optional
    sqlalchemy.Column("git_commit_id", sqlalchemy.String), # git Optional    
    sqlalchemy.Column("solved", sqlalchemy.Boolean), 
    sqlalchemy.Column("send_date", sqlalchemy.DateTime), 
    sqlalchemy.Column("tests_results", sqlalchemy.PickleType),
)
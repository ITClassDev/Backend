import sqlalchemy
from .base import metadata, engine

market = sqlalchemy.Table(
    "market_products", 
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("title", sqlalchemy.String()),
    sqlalchemy.Column("cost", sqlalchemy.Integer()),
    sqlalchemy.Column("remain_amount", sqlalchemy.Integer()),
    sqlalchemy.Column("about", sqlalchemy.String()),
    sqlalchemy.Column("image_path", sqlalchemy.String())
)

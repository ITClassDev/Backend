# Run this script in docker to migrate all new tables/updates (deleting old revision id)
from app import settings
from sqlmodel import create_engine, SQLModel
from sqlalchemy import text
import os

db_connection_str = settings.db_async_connection_str.replace("postgresql+asyncpg", "postgresql")

engine = create_engine(db_connection_str)
SQLModel.metadata.create_all(engine)
with engine.connect() as con:
    rs = con.execute(text('DROP TABLE alembic_version'))


# os.system("./migrate.sh Docker UPD")
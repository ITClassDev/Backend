from sys import modules
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from app import settings
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import create_engine, SQLModel, Session
from app.assigments.models import Contest



db_connection_str = settings.db_async_connection_str

#engine = create_engine(db_connection_str)
#SQLModel.metadata.create_all(engine)\

if "pytest" in modules:
    db_connection_str = settings.db_async_test_connection_str


async_engine = create_async_engine(
    db_connection_str,
    echo=False,
    future=True
)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        
        yield session

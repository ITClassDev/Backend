import uuid as uuid_pkg
from pydantic import BaseModel
from app.core.models import TimestampModel, UUIDModel
from sqlmodel import Field, Relationship
from typing import List

class Group(UUIDModel, TimestampModel, table=True):
    __tablename__ = "groups"
    name: str = Field(nullable=False)
    color: str = Field(nullable=False, default="#3B83BD")
    
    users: List["User"] = Relationship(back_populates="group")


from sqlalchemy import Column, JSON
from sqlmodel import Field
import uuid as uuid_pkg
from app.core.models import TimestampModel, UUIDModel

class Notification(UUIDModel, TimestampModel, table=True):
    __tablename__ = "notifications"  # type: ignore
    toUser: uuid_pkg.UUID = Field(nullable=False, foreign_key="users.uuid")
    type: int = Field(default=0, nullable=False)
    viewed: bool = Field(default=False, nullable=False)
    data: dict = Field(sa_column=Column(
        "data",
        JSON
    ))
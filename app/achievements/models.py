from sqlalchemy import Column, event
from sqlalchemy.databases import postgres
from sqlmodel import Field, SQLModel
import uuid as uuid_pkg
from datetime import datetime
from app.core.models import TimestampModel, UUIDModel

achievement_type = postgres.ENUM(
    "olimpiad",
    "event",
    name=f"eventType"
)


@event.listens_for(SQLModel.metadata, "before_create")
def _create_enums(metadata, conn, **kw):
    achievement_type.create(conn, checkfirst=True)


class Achievement(UUIDModel, TimestampModel, table=True):
    __tablename__ = "achievements"  # type: ignore
    toUser: uuid_pkg.UUID = Field(foreign_key="users.uuid", nullable=False)
    acceptedBy: uuid_pkg.UUID = Field(foreign_key="users.uuid", nullable=True)
    
    eventType: str = Field(sa_column=Column(
        "role",
        achievement_type,
        nullable=False,
        default="event"
    ))
    title: str = Field(nullable=False, max_length=500)
    attachmentName: str = Field(nullable=False)
    description: str = Field(nullable=False, max_length=5000)
    points: int = Field(nullable=True)
    acceptedAt: datetime = Field(nullable=True)

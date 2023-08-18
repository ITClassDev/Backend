from sqlalchemy import Column, event, ForeignKey
from sqlalchemy.databases import postgres
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid as uuid_pkg
from datetime import datetime
from app.core.models import TimestampModel, UUIDModel
from typing import Optional

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
    toUser: uuid_pkg.UUID = Field(
        nullable=False,
        sa_column=Column(UUID(as_uuid=1), ForeignKey("users.uuid", ondelete="CASCADE")) 
    )
    user: Optional["User"] = Relationship(back_populates="achievements")
    acceptedBy: Optional[uuid_pkg.UUID] = Field(nullable=True)
    
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

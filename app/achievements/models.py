from sqlalchemy import Column, event
from sqlalchemy.orm import relationship
from sqlalchemy.databases import postgres
from sqlmodel import Field, SQLModel, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid as uuid_pkg
from datetime import datetime
from app.core.models import TimestampModel, UUIDModel
from app.users.models import User

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
    toUserId: uuid_pkg.UUID = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    toUser: object = relationship('User', foreign_keys=[toUserId])


    acceptedById: uuid_pkg.UUID = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    acceptedBy: object = relationship('User', foreign_keys=[acceptedById])
    
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
    acceptedAt: datetime = Field(default_factory=datetime.utcnow, nullable=True)

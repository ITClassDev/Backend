from sqlalchemy import Column, JSON, ForeignKey, event
from sqlmodel import Field, SQLModel, Relationship
import uuid as uuid_pkg
from app.core.models import TimestampModel, UUIDModel
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from sqlalchemy.databases import postgres


notification_type = postgres.ENUM(
    "info",
    "warning",
    "danger",
    name=f"user_role"
)


@event.listens_for(SQLModel.metadata, "before_create")
def _create_enums(metadata, conn, **kw):
    notification_type.create(conn, checkfirst=True)


class Notification(UUIDModel, TimestampModel, table=True):
    __tablename__ = "notifications"  # type: ignore
    toUser: uuid_pkg.UUID = Field(
        nullable=False,
        sa_column=Column(UUID(as_uuid=1), ForeignKey("users.uuid", ondelete="CASCADE")) 
    )
    type: int = Field(default=0, nullable=False)
    viewed: bool = Field(default=False, nullable=False)
    user: Optional["User"] = Relationship(back_populates="notifications")
    data: dict = Field(sa_column=Column(
        "data",
        JSON
    ))

class SystemNotification(UUIDModel, TimestampModel, table=True):
    __tablename__ = "system_notifications"
    active: bool = Field(nullable=False, default=False)
    type: 
    
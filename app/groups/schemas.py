from pydantic import BaseModel
import uuid as uuid_pkg


class GroupCreate(BaseModel):
    name: str
    color: str


class GroupRead(BaseModel):
    uuid: uuid_pkg.UUID
    name: str
    color: str

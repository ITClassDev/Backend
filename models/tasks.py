from pydantic import BaseModel
from typing import Optional
import datetime

class Task(BaseModel):
    id: Optional[int] = None
    author_id: int
    title: str
    text: str
    time_limit: int
    memory_limit: int
    is_day_challenge: bool
    tests: dict

class TaskIn(BaseModel):
    title: str
    text: str
    time_limit: int
    memory_limit: int
    is_day_challenge: bool
    tests: dict

from pydantic import BaseModel
from typing import Optional, List

class Contest(BaseModel):
    id: Optional[int] = None
    author_id: int
    title: str
    description: str
    tasks_ids_list: List[int]
    users_ids_tags: List[int]

class ContestIn(BaseModel):
    title: str
    description: str
    tasks_ids_list: List[int]
    users_ids_tags: List[int]

class SubmitContest(BaseModel):
    git_url: str
    contest_id: int
    language: str
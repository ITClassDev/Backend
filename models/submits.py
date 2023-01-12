from pydantic import BaseModel
from typing import Optional

class Submit(BaseModel):
    id: Optional[int] = None
    user_id: int
    status: int
    task_id: int
    source: str
    refer_to: Optional[int] = None
    git_commit_id: Optional[str] = None
    solved: bool
    tests_results: dict

    
class SubmitIn(BaseModel):
    status: int
    task_id: int
    source: str
    refer_to: Optional[int] = None
    git_commit_id: Optional[str] = None
    solved: bool
    tests_results: dict
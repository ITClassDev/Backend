from pydantic import BaseModel
from typing import Optional, List
import datetime

class Submit(BaseModel):
    id: Optional[int] = None
    user_id: int
    status: int
    task_id: int
    source: str
    refer_to: Optional[int] = None
    git_commit_id: Optional[str] = None
    solved: bool
    tests_results: Optional[List[dict]] = None
    send_date: datetime.datetime
    

# class SubmitIn(BaseModel):
#     status: int
#     task_id: int
#     source: str
#     refer_to: Optional[int] = None
#     git_commit_id: Optional[str] = None
#     solved: bool
#     tests_results: dict
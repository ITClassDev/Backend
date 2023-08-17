from fastapi import APIRouter, Depends
import uuid as uuid_pkg
from app.assigments.schemas import TaskCreate
from app.users.models import User
from app.assigments.models import Task
from app.auth.dependencies import get_current_user, atleast_teacher_access
from app.assigments.crud import TasksCRUD, ContestsCRUD, SubmitsCRUD
from app.assigments.dependencies import get_contests_crud, get_submits_crud, get_tasks_crud
from typing import List

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
async def get_all_tasks(tasks: TasksCRUD = Depends(get_tasks_crud), current_user: User = Depends(atleast_teacher_access)):
    return await tasks.get_all()

@router.get("/tasks/{uuid}", response_model=Task)
async def get_task(uuid: uuid_pkg.UUID, tasks: TasksCRUD = Depends(get_tasks_crud)):
    return await tasks.get(uuid)

@router.put("/tasks")
async def create_task(task: TaskCreate, tasks: TasksCRUD = Depends(get_tasks_crud), current_user: User =  Depends(atleast_teacher_access)):
    return await tasks.create(task, current_user.uuid)

@router.get("/tasks/search")
async def search_task(query: str):
    pass

@router.get("/tasks/challenge")
async def get_day_challenge():
    pass

@router.get("/tasks/challenge/leaderboard")
async def get_day_challenge_leaderboard():
    pass

@router.post("/tasks/submission/{uuid}")
async def get_submit_details(uuid: uuid_pkg.UUID):
    pass

@router.post("/tasks/challenge/submit")
async def submit_day_challenge():
    pass

@router.get("/tasks/submits/{uuid}")
async def get_current_user_task_submits(uuid: uuid_pkg.UUID):
    pass

@router.get("/homeworks")
async def get_active_homeworks_for_current_user(uuid: uuid_pkg.UUID):
    pass

@router.post("/homeworks/submit")
async def submit_homework(uuid: uuid_pkg.UUID):
    pass


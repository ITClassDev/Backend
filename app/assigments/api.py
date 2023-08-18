from fastapi import APIRouter, Depends
import uuid as uuid_pkg
from app.assigments.schemas import TaskCreate, TaskSearch
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

@router.put("/tasks")
async def create_task(task: TaskCreate, tasks: TasksCRUD = Depends(get_tasks_crud), current_user: User =  Depends(atleast_teacher_access)):
    return await tasks.create(task, current_user.uuid)

@router.get("/tasks/search", response_model=List[TaskSearch])
async def search_task(query: str, tasks: TasksCRUD = Depends(get_tasks_crud)):
    return await tasks.search(query)

@router.get("/tasks/challenge")
async def get_day_challenge(tasks: TasksCRUD = Depends(get_tasks_crud)):
    return await tasks.get_day_challenge()

@router.patch("/tasks/challenge/set/{uuid}")
async def set_challenge_task(uuid: uuid_pkg.UUID, tasks: TasksCRUD = Depends(get_tasks_crud), current_user: User = Depends(atleast_teacher_access)):
    return await tasks.set_challenge(uuid)

@router.get("/tasks/challenge/leaderboard")
async def get_day_challenge_leaderboard():
    pass

@router.get("/tasks/submission/{uuid}")
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

@router.get("/tasks/{uuid}", response_model=Task)
async def get_task(uuid: uuid_pkg.UUID, tasks: TasksCRUD = Depends(get_tasks_crud)):
    return await tasks.get(uuid)
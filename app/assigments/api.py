from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi import status as http_status
import uuid as uuid_pkg
from app.assigments.schemas import TaskCreate, TaskSearch
from app.users.models import User
from app.assigments.models import Task
from app.auth.dependencies import get_current_user, atleast_teacher_access
from app.assigments.crud import TasksCRUD, ContestsCRUD, SubmitsCRUD
from app.assigments.models import Submit
from app.assigments.dependencies import get_contests_crud, get_submits_crud, get_tasks_crud
from typing import List
import os
from app.core.files import upload_file
from app import settings


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

@router.get("/tasks/submit/{uuid}")
async def get_submit_details(uuid: uuid_pkg.UUID, current_user: User = Depends(get_current_user), submits: SubmitsCRUD = Depends(get_submits_crud)):
    return await submits.get(uuid, current_user.uuid)

@router.post("/tasks/challenge/submit")
async def submit_day_challenge(source: UploadFile, current_user: User = Depends(get_current_user), submits: SubmitsCRUD = Depends(get_submits_crud)):
    uploaded_source = await upload_file(source, ["py", "cpp"], os.path.join(settings.user_storage, "tasks_source_codes"))
    if uploaded_source["status"]:
        submit = await submits.submit_day_challenge(uploaded_source["file_name"], current_user.uuid)
        return submit
    raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Invalid file extension")

@router.get("/tasks/challenge/submits")
async def get_current_user_challenge_submits(current_user: User = Depends(get_current_user), submits: SubmitsCRUD = Depends(get_submits_crud)):
    return await submits.day_challenge_user_submits(current_user.uuid)


@router.get("/tasks/{uuid}/submits")
async def get_current_user_task_submits(uuid: uuid_pkg.UUID, current_user: User = Depends(get_current_user), submits: SubmitsCRUD = Depends(get_submits_crud)):
    return await submits.get_users_for_tasks(uuid, current_user.uuid)

@router.get("/homeworks")
async def get_active_homeworks_for_current_user(uuid: uuid_pkg.UUID):
    pass

@router.post("/homeworks/submit")
async def submit_homework(uuid: uuid_pkg.UUID):
    pass

@router.get("/tasks/{uuid}", response_model=Task)
async def get_task(uuid: uuid_pkg.UUID, tasks: TasksCRUD = Depends(get_tasks_crud)):
    return await tasks.get(uuid)
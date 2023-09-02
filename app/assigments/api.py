from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi import status as http_status
import uuid as uuid_pkg
from app.assigments.schemas import TaskCreate, TaskSearch, ContestSubmitGithub, SubmitSourceCode
from app.users.models import User
from app.assigments.models import Task
from app.auth.dependencies import get_current_user, atleast_teacher_access
from app.assigments.crud import TasksCRUD, ContestsCRUD, SubmitsCRUD
from app.assigments.models import Submit, Contest
from app.assigments.dependencies import get_contests_crud, get_submits_crud, get_tasks_crud
from typing import List
import os
from app.core.files import upload_file
from app import settings
from app.assigments.schemas import TaskLeaderBoard, ContestCreate
import threading
import app.assigments.checker_api as checker_api
import asyncio

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

@router.patch("/tasks/challenge/set/{uuid}", response_model=Task)
async def set_challenge_task(uuid: uuid_pkg.UUID, tasks: TasksCRUD = Depends(get_tasks_crud), current_user: User = Depends(atleast_teacher_access)):
    return await tasks.set_challenge(uuid)

@router.get("/tasks/challenge/leaderboard", response_model=List[TaskLeaderBoard])
async def get_day_challenge_leaderboard(tasks: TasksCRUD = Depends(get_tasks_crud)):
    challenge = await tasks.get_day_challenge()
    return await tasks.task_leaderboard(challenge.uuid)

@router.get("/submit/{uuid}/source", response_model=SubmitSourceCode)
async def submit_source(uuid: uuid_pkg.UUID, _: User = Depends(atleast_teacher_access), submits: SubmitsCRUD = Depends(get_submits_crud)):
    return await submits.get_source_code(uuid)

@router.delete("/submit/{uuid}/reject", response_model=None)
async def reject_submit(uuid: uuid_pkg.UUID, _: User = Depends(atleast_teacher_access), submits: SubmitsCRUD = Depends(get_submits_crud)):
    await submits.reject(uuid)

@router.post("/tasks/challenge/submit")
async def submit_day_challenge(source: UploadFile, current_user: User = Depends(get_current_user), submits: SubmitsCRUD = Depends(get_submits_crud)):
    uploaded_source = await upload_file(source, ["py", "cpp"], os.path.join(settings.user_storage, "tasks_source_codes"))
    if not uploaded_source["size"]: raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Empty source code")
    loop = asyncio.get_event_loop()
    if uploaded_source["status"]:
        submit, task = await submits.submit_day_challenge(uploaded_source["file_name"], current_user.uuid)
        env = {"cpu_time_limit": task.timeLimit, "real_time_limit": task.timeLimit + 0.5, "memory_limit": task.memoryLimit}
        payload = {"source_code_path": uploaded_source["file_name"], "language": {"py": 0, "cpp": 1}[uploaded_source["extension"]], "tests": task.tests, "submit_id": str(submit.uuid), "env": env}
        threading.Thread(target=lambda: checker_api.challenge(payload, submits.checker_callback, loop)).start()
        return submit
    raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Invalid file extension")

@router.get("/tasks/challenge/submits")
async def get_current_user_challenge_submits(current_user: User = Depends(get_current_user), submits: SubmitsCRUD = Depends(get_submits_crud)):
    return await submits.day_challenge_user_submits(current_user.uuid)


@router.get("/tasks/{uuid}/submits")
async def get_current_user_task_submits(uuid: uuid_pkg.UUID, current_user: User = Depends(get_current_user), submits: SubmitsCRUD = Depends(get_submits_crud)):
    return await submits.get_users_for_tasks(uuid, current_user.uuid)

@router.patch("/tasks/{uuid}")
async def update_task_data(uuid: uuid_pkg.UUID, task: TaskCreate, current_user: User = Depends(atleast_teacher_access), tasks: TasksCRUD = Depends(get_tasks_crud)):
    return await tasks.update(uuid, task)


@router.get("/contests")
async def get_all_contests_for_admin(_: User = Depends(atleast_teacher_access), contests: ContestsCRUD = Depends(get_contests_crud)):
    return await contests.get_all()

@router.get("/contests/available")
async def get_active_contests_for_current_user(current_user: User = Depends(get_current_user), contests: ContestsCRUD = Depends(get_contests_crud)):
    return await contests.get_active_for_user(current_user.groupId, current_user.learningClass)

@router.put("/contests", response_model=Contest)
async def create_contest(contest: ContestCreate, current_user: User = Depends(atleast_teacher_access), contests: ContestsCRUD = Depends(get_contests_crud)):
    return await contests.create(contest, current_user.uuid)

@router.get("/contests/{uuid}")
async def get_contest_data(uuid: uuid_pkg.UUID, _: User = Depends(get_current_user), contests: ContestsCRUD = Depends(get_contests_crud)):
    return await contests.get(uuid)

@router.get("/contests/{contest_uuid}/task/{task_uuid}/submits")
async def get_current_user_task_submits_refered_for_contest(contest_uuid: uuid_pkg.UUID, task_uuid: uuid_pkg.UUID, current_user: User = Depends(get_current_user), submits: SubmitsCRUD = Depends(get_submits_crud)):
    return await submits.get_users_refered_for_contest_task(task_uuid, contest_uuid, current_user.uuid)


@router.post("/contests/submit")
async def submit_homework(submit: ContestSubmitGithub, submits: SubmitsCRUD = Depends(get_submits_crud), current_user: User = Depends(get_current_user)):
    return await submits.submit_contest(submit, current_user.uuid)

@router.get("/tasks/{uuid}", response_model=Task)
async def get_task(uuid: uuid_pkg.UUID, tasks: TasksCRUD = Depends(get_tasks_crud), current_user: User = Depends(get_current_user)):
    return await tasks.get(uuid, False if current_user.role in ["teacher", "admin"] else True)

@router.get("/tasks/submit/{uuid}", response_model=Submit)
async def get_submit_details(uuid: uuid_pkg.UUID, current_user: User = Depends(get_current_user), submits: SubmitsCRUD = Depends(get_submits_crud)):
    return await submits.get(uuid, current_user.uuid)
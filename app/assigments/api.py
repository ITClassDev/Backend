from fastapi import APIRouter
import uuid as uuid_pkg
from app.assigments.schemas import TaskCreate
from app.assigments.crud import TasksCRUD, ContestsCRUD, SubmitsCRUD

router = APIRouter()

@router.get("/tasks")
async def get_all_tasks():
    pass

@router.get("/tasks/{uuid}")
async def get_task(uuid: uuid_pkg.UUID):
    pass

@router.put("/tasks")
async def create_task(task: TaskCreate, tasks: TasksCRUD):
    return await tasks.create(task)

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


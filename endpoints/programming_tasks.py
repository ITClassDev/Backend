from fastapi import APIRouter, Depends
from repositories.users import UserRepository
from repositories.tasks import TasksRepository
from models.tasks import TaskIn
from models.user import User
from .depends import get_tasks_repository, get_current_user

router = APIRouter()

### Tasks ###
@router.get("/task/{task_id}")
async def get_task_info(task_id: int, tasks: TasksRepository = Depends(get_tasks_repository)):
    return await tasks.get_by_id(task_id)

@router.put("/task/add") # Teacher level
async def get_task_info(task_data: TaskIn, tasks: TasksRepository = Depends(get_tasks_repository), current_user: User = Depends(get_current_user)):
    if current_user.userRole > 0:
        task_id = await tasks.add(task_data, current_user.id)
        return {"task_id": task_id}

### Day Challenge

@router.get("/day_challenge/current")
async def get_day_challenge(tasks: TasksRepository = Depends(get_tasks_repository)):
    return await tasks.get_day_challenge()
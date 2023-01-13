from fastapi import APIRouter, Depends, UploadFile
from repositories.users import UserRepository
from repositories.tasks import TasksRepository
from models.tasks import TaskIn
from models.user import User
from .depends import get_tasks_repository, get_current_user
from core.utils.files import upload_file
import os
from core.config import USERS_STORAGE
#import sys
#sys.path.append("../")
import PyChecker.checker as CheckerBase

router = APIRouter()

# Create checker object
Checker = CheckerBase.Checker()



### Tasks ###
@router.get("/task/{task_id}")
async def get_task_info(task_id: int, tasks: TasksRepository = Depends(get_tasks_repository)):
    return await tasks.get_by_id(task_id)

@router.put("/task/add") # Teacher level
async def get_task_info(task_data: TaskIn, tasks: TasksRepository = Depends(get_tasks_repository), current_user: User = Depends(get_current_user)):
    if current_user.userRole > 0:
        task_id = await tasks.add(task_data, current_user.id)
        return {"task_id": task_id}

### Day Challenge ###
@router.get("/day_challenge/current")
async def get_day_challenge(tasks: TasksRepository = Depends(get_tasks_repository)):
    task_data = await tasks.get_day_challenge()
    tests_data_dict = {**task_data}
    demo_tests = []
    ind = 0
    for test in tests_data_dict["tests"]:
        if "demo" in test and test["demo"]:
            demo_tests.append({**test, "key": ind})
            ind += 1
    tests_data_dict["tests"] = demo_tests
    return {**tests_data_dict, "tests": demo_tests}

@router.post("/day_challenge/submit")
async def submit_day_challenge(file: UploadFile, tasks: TasksRepository = Depends(get_tasks_repository), current_user: User = Depends(get_current_user)):
    allowed_extensions = ["cpp", "py"]  # c++ files and python files
    uploaded_source = await upload_file(file, allowed_extensions, os.path.join(USERS_STORAGE, "tasks_source_codes"))
    submit_id = await tasks.submit_day_challenge(current_user.id, uploaded_source, Checker)
    return {"submit_id": submit_id}

@router.get("/task/my_submits/{task_id}")
async def get_my_submits(task_id: int, current_user: User = Depends(get_current_user), tasks: TasksRepository = Depends(get_tasks_repository)):
    submits = await tasks.get_task_submits(current_user.id, task_id)
    return submits


### Contest ###

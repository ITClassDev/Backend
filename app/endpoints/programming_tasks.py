from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from repositories.users import UserRepository
from repositories.tasks import TasksRepository
from models.tasks import TaskIn
from models.user import User
from models.contests import ContestIn, SubmitContest
from .depends import get_tasks_repository, get_current_user
from core.utils.files import upload_file
import os
from core.config import USERS_STORAGE
import multiprocessing
import socket
import json


# FIXIT Shit style
class Checker:
    def __init__(self, host="localhost", port=7778) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def listen(self, day_challenge_callback, homework_callback):
        print("Started listening")
        while True:
            data = self.sock.recv(1024)
            if data:
                data = json.loads(data)
                print(data)
    
    def day_challenge(self, submit_id, source, test):
        pass


router = APIRouter()

# Create checker object
# Checker = CheckerBase.Checker()
# Test code
if 0:
    checker = Checker()
    callback_0 = lambda x: print("Homework")
    callback_1 = lambda x: print("Contest")
    checker_listen_process = multiprocessing.Process(target=lambda: checker.listen(callback_0, callback_1))
    checker_listen_process.start()

### Tasks ###
@router.get("/task/{task_id}/")
async def get_task_info(task_id: int, tasks: TasksRepository = Depends(get_tasks_repository)):
    task_data = await tasks.get_by_id_full(task_id)
    if task_data:
        tests_data_dict = {**task_data}
        demo_tests = []
        ind = 0
        for test in tests_data_dict["tests"]:
            if "demo" in test and test["demo"]:
                demo_tests.append({**test, "key": ind})
                ind += 1
        tests_data_dict["tests"] = demo_tests
        return tests_data_dict
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No task with such id")

@router.put("/task/add/") # Teacher level
async def get_task_info(task_data: TaskIn, tasks: TasksRepository = Depends(get_tasks_repository), current_user: User = Depends(get_current_user)):
    if current_user.userRole > 0:
        task_id = await tasks.add(task_data, current_user.id)
        return {"task_id": task_id}

@router.get("/tasks/all/") # All tasks
async def get_all_tasks(tasks: TasksRepository = Depends(get_tasks_repository), current_user: User = Depends(get_current_user)):
    if current_user.userRole > 0:
        return await tasks.get_all()
    else:
        return {"status": False}

### Day Challenge ###
@router.get("/day_challenge/current/")
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

@router.post("/day_challenge/submit/")
async def submit_day_challenge(file: UploadFile, tasks: TasksRepository = Depends(get_tasks_repository), current_user: User = Depends(get_current_user)):
    allowed_extensions = ["cpp", "py"]  # c++ files and python files
    uploaded_source = await upload_file(file, allowed_extensions, os.path.join(USERS_STORAGE, "tasks_source_codes"))
    submit_id = await tasks.submit_day_challenge(current_user.id, uploaded_source, Checker)
    # Run checker
    return {"submit_id": submit_id}

@router.get("/task/my_submits/{task_id}/")
async def get_my_submits(task_id: int, current_user: User = Depends(get_current_user), tasks: TasksRepository = Depends(get_tasks_repository)):
    submits = await tasks.get_task_submits(current_user.id, task_id)
    return submits


### Contest ###
@router.put("/homework/create/")
async def create_homework(contest_data: ContestIn, current_user: User = Depends(get_current_user), tasks: TasksRepository = Depends(get_tasks_repository)):
    if current_user.userRole > 0:
        contest_id = await tasks.create_contest(contest_data, current_user.id)
        return {"contest_id": contest_id}
    else:
        return {"status": False}

@router.get("/homework/get/")
async def get_homework(contest_id: int, tasks: TasksRepository = Depends(get_tasks_repository)):
    contest_data = await tasks.get_contest_tasks(contest_id)
    tasks_titles = []
    for task in contest_data.tasks_ids_list:
        task_data = await tasks.get_by_id_full(task)
        tasks_titles.append(task_data.title)
    contest_data = {**contest_data}
    # 
    # tests_data_dict = {**task_data}
    # demo_tests = []
    # ind = 0
    # for test in tests_data_dict["tests"]:
    #     if "demo" in test and test["demo"]:
    #         demo_tests.append({**test, "key": ind})
    #         ind += 1
    # tests_data_dict["tests"] = demo_tests
    contest_data["tasks_titles"] = tasks_titles
    return contest_data
    
@router.post("/homework/submit/")
async def send_submit(submit_data: SubmitContest, current_user: User =  Depends(get_current_user), tasks: TasksRepository = Depends(get_tasks_repository)):
    submit_id = await tasks.submit_contest(submit_data.contest_id, submit_data.git_url, current_user.id, submit_data.language, Checker)
    return {"submit_id": submit_id}

@router.get("/homework/get_task_submits/")
async def get_task_submits(task_id: int, contest_id: int, current_user: User = Depends(get_current_user), tasks: TasksRepository = Depends(get_tasks_repository)):
    return await tasks.get_contest_task_submits(task_id, contest_id)

@router.get("/submission/details/")
async def submission_details(submission_id: int, tasks: TasksRepository = Depends(get_tasks_repository)):
    data = await tasks.get_submission_details(submission_id)
    with open(os.path.join(USERS_STORAGE, "tasks_source_codes", data.source.split(":")[1]), "r") as file:
        source = file.read()
    return {"task": data, "source": source}

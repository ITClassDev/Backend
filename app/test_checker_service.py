from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from PyChecker.checker import Checker
import os

app = FastAPI(title="ShTP Checker EPICBOX Service", version="0.0.1 EPICBOX")

checker = Checker()

class OneTask(BaseModel):
    source_code_path: str
    language: int
    tests: list
    env: dict
    submit_id: int

@app.get("/")
async def index():
    return {"status": "Checker is ready"}

@app.post("/challenge")
async def check_challenge(payload: OneTask):
    return checker.check_one_task_thread(os.path.join("/home/stephan/Progs/ItClassDevelopment/Backend/app/static/users_data/uploads/tasks_source_codes", payload.source_code_path), payload.language, payload.tests, payload.env, payload.submit_id)


if __name__ == "__main__":
    uvicorn.run("test_checker_service:app", port=7777, host="localhost", reload=True, headers=[("server", "Docker")])
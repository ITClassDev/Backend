from fastapi import FastAPI
import uvicorn
from core.config import SERVER_HOST, SERVER_PORT
from db.base import database
from endpoints import users

app = FastAPI(title="ITC REST API")
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
async def index():
    return {"status": True, "data": "Hello from ITC backend!"}

@app.on_event("startup")
async def startup():
    await database.connect()
    

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



if __name__ == "__main__":
    uvicorn.run("main:app", port=SERVER_PORT, host=SERVER_HOST, reload=True)
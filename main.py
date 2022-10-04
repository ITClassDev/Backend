from fastapi import FastAPI
import uvicorn
from core.config import SERVER_HOST, SERVER_PORT

app = FastAPI()

@app.get("/")
async def index():
    return {"status": True, "data": "It works"}

@app.on_event("startup")
async def startup():
    print("Starting")

@app.on_event("shutdown")
async def shutdown():
    print("Stopping")



if __name__ == "__main__":
    uvicorn.run("main:app", port=SERVER_PORT, host=SERVER_HOST, reload=True)
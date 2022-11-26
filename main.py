from fastapi import FastAPI
import uvicorn
from core.config import SERVER_HOST, SERVER_PORT
from db.base import database
from endpoints import users, auth
from endpoints.mobile import (
    users as users_mobile,
    auth as auth_mobile
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from core.config import USERS_STORAGE, API_VER

app = FastAPI(title="ITC REST API", version="0.0.1")
app.mount("/storage", StaticFiles(directory=USERS_STORAGE), name="storage") # User data storage(local)

# FIXIT Security ALERT; Remove on prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Native JSON REST API
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Mobile Protocol buffer API
app.include_router(users_mobile.router, prefix="/mobile/users", tags=["Protobuf(NO Swagger)"])
app.include_router(auth_mobile.router, prefix="/mobile/auth", tags=["Protobuf(NO Swagger)"])


@app.get("/")
async def index():
    return {"status": True, "api_ver": API_VER, "endpoints": {"storage": "/storage", "mobile": "/mobile/"}}

@app.get("/mobile")
async def mobile_placeholder():
    return {"status": True, "about": "This is an optimized version of our API for mobile devices. This version of the api completely repeats the behavior of the main version. The only difference is that in the main version we use the usual json as serialization, but in this version we use the buffers protocol. You can learn more in our documentation."}

@app.on_event("startup")
async def startup():
    await database.connect()
    

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



if __name__ == "__main__":
    uvicorn.run("main:app", port=SERVER_PORT, host=SERVER_HOST, reload=True, headers=[("server", "PoweredByPutincev")])
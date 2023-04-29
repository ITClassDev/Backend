from fastapi import FastAPI
import uvicorn
from core.config import SERVER_HOST, SERVER_PORT, ROOT_PATH
from db.base import database
from endpoints import users, auth, achievements, oauth, admin, notifications, programming_tasks, polls, notifications
from endpoints.mobile import (
    users as users_mobile,
    auth as auth_mobile
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from core.config import USERS_STORAGE, API_VER
from core.utils.system import get_system_status

# Docs metadata
description_metadata = '''
Welcome to ShTP API Docs!

[ShTP API Source Code](https://github.com/ItClassDev/Backend)
'''


tags_metadata = [
    {
        "name": "users",
        "description": "CRUD Operations with users, users groups. To use some endpoints you have to auth via *auth/login* endpoint."
    },
    {
        "name": "auth",
        "description": "Generate JWT token for access to private endpoints and get current user via JWT token."
    }
]

app = FastAPI(title="ITC REST API", version=API_VER, openapi_tags=tags_metadata, description=description_metadata, docs_url='/docs/', root_path=ROOT_PATH)
app.mount("/storage", StaticFiles(directory=USERS_STORAGE), name="storage")  # User data storage(local)

# FIXIT Security ALERT; Remove on prod
# We have to enable only frontend domain
# But we didn't have it now
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
app.include_router(achievements.router, prefix="/achievements", tags=["achievements"])
app.include_router(oauth.router, prefix="/oauth", tags=["oauth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(programming_tasks.router, prefix="/programming_tasks", tags=["programming_checker"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
app.include_router(polls.router, prefix="/polls", tags=["polls"])

# Mobile Protocol buffer API
app.include_router(users_mobile.router, prefix="/mobile/users", tags=["Protobuf(NO Swagger)"])
app.include_router(auth_mobile.router, prefix="/mobile/auth", tags=["Protobuf(NO Swagger)"])


@app.get("/")
async def index():
    cpu_load, ram_load = get_system_status()
    return {"status": True, "api_ver": API_VER, "endpoints": {"storage": "/storage", "mobile": "/mobile/"},
            "system_status": {"cpu": cpu_load, "ram": ram_load}}


@app.get("/mobile")
async def mobile_placeholder():
    return {"status": True,
            "about": "This is an optimized version of our API for mobile devices.This version of the api completely repeats the behavior of the main version.The only difference is that in the main version we use the usual json as serialization, but in this version we use the buffers protocol.You can learn more in our documentation."}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=SERVER_PORT, host=SERVER_HOST, reload=True, headers=[("server", "PoweredByPutincev")], root_path=ROOT_PATH)

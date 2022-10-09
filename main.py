from fastapi import FastAPI
import uvicorn
from core.config import SERVER_HOST, SERVER_PORT
from db.base import database
from endpoints import users, auth, market
from endpoints.mobile import (
    users as users_mobile,
    auth as auth_mobile
)

app = FastAPI(title="ITC REST API")
# For DEV !
from fastapi.middleware.cors import CORSMiddleware
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
app.include_router(market.router, prefix="/market", tags=["market"])

# Mobile Protocol buffer API
app.include_router(users_mobile.router, prefix="/mobile/users", tags=["Protobuf(NO Swagger)"])
app.include_router(auth_mobile.router, prefix="/mobile/auth", tags=["Protobuf(NO Swagger)"])


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
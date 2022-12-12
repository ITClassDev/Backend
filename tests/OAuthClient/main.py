# Test OAuth app using FastAPI

from fastapi import FastAPI
import uvicorn
import requests

def getOAuthedUser(api="http://localhost:8080/oauth/get_user"):
    data = requests.get("")


app = FastAPI()


@app.get("/login_with_shtp") # endpoint
async def login_with_shtp(access_token: int):
    print("New login with token:", access_token)
    return {"data_from_shtp": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=3232, host="localhost", reload=True)
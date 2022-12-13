# Test OAuth app using FastAPI

from fastapi import FastAPI
import uvicorn
import requests

async def getOAuthedUser(token: str, api: str="http://localhost:8080/oauth/get_user") -> int:
    data = requests.get(f"{api}/{token}").json()
    if data["status"]:
        return data["user_id"]
    else: # invalid token
        return -1


app = FastAPI() # init fastapi app


@app.get("/login_with_shtp") # endpoint to login (redirect url)
async def login_with_shtp(access_token: str): # get param -> access token
    print("[DEBUG] New login with token:", access_token)
    shtp_user_id = await getOAuthedUser(token=access_token)
    if shtp_user_id != -1:
        print("[DEBUG] Confirmed user id:", shtp_user_id)
    else:
        print("[DEBUG] Can't get user id; invalid token")
    
    return {"data_from_shtp": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=3232, host="localhost", reload=True) # run async web server
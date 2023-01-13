# Test OAuth app using FastAPI
# This is simple 'raw' example
# But you can check our PyAPI wrapper for SHTP API

from fastapi import FastAPI
import uvicorn
import requests
from typing import List, Dict
from fastapi.responses import HTMLResponse


# Fake database as json to store shtp_id and real user id
# Real user id's are differ from shtp to demonstrate OAuth scheme
FAKE_DB_USERS = [
    {"id": 123, "name": "Stephan Zhdanov", "shtp_id": 6},
    {"id": 232, "name": "Test user", "shtp_id": 2}
]

# Like sql select function (utility)
async def findUserByShtp(db: List[Dict], shtp_id: int):
    for user in db:
        if user["shtp_id"] == shtp_id:
            return user

# Make request to shtp api to get verified answer about user id
async def getOAuthedUser(token: str, api: str="http://localhost:8080/oauth/get_user") -> int:
    data = requests.get(f"{api}/{token}").json()
    if data["status"]:
        return data["user_id"]
    else: # invalid token
        return -1

# init fastapi app
app = FastAPI() 

# endpoint to login (redirect url)
# in our case it is root endpoint
@app.get("/", response_class=HTMLResponse)
async def login_with_shtp(access_token: str): # get param -> access token
    # For extra security you can check the domain/ip address of requester, to be sure
    print("[DEBUG] New login with token:", access_token)
    status = "FAIL"
    shtp_user_id = await getOAuthedUser(token=access_token, api="http://10.12.0.84:8080/oauth/get_user")
    real_user_id = "FAIL"
    user_real_name= "FAIL"
    if shtp_user_id != -1:
        print("[DEBUG] Confirmed user id:", shtp_user_id)
        real_user_id = await findUserByShtp(FAKE_DB_USERS, shtp_user_id)
        print("[DEBUG] Real user linked to this shtp id:", real_user_id)
        user_real_name = real_user_id["name"]
        status = "OK"
    else:
        print("[DEBUG] Can't get user id; invalid token")
    
    return f"""
    <html>
        <head>
            <title>OAuth test client</title>
        </head>
        <body>
            <h1>Data from shtp!</h1>
            <p>Status: {status}</p>
            <p>User id in our db: {shtp_user_id}</p>
            <p>User Name: {user_real_name}</p>
            <h2>Local site database</h2>
            <code>
                [
                    {{"id": 123, "name": "Stephan Zhdanov", "shtp_id": 1}},
                    {{"id": 232, "name": "Test user", "shtp_id": 2}}
                ]
            </code>
        </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run("main:app", port=3456, host="0.0.0.0", reload=True) # run async web server
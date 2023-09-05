import requests
from app import settings
import json
import time

def challenge(payload, save, loop):
    data = requests.post(f"{settings.checker_api}/challenge", json=payload, timeout=60).json()
    save(data, loop)

def homework(payload, save, loop):
    # print(json.dumps(payload))
    data = requests.post(f"{settings.checker_api}/homework", data=json.dumps(payload), timeout=6000).json()
    # print(data)
    save(data, loop)

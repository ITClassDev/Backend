import requests
from app import settings

def challenge(payload, save, loop):
    data = requests.post(f"{settings.checker_api}/challenge", json=payload, timeout=60).json()
    save(data, loop)

def homework(payload, save, loop):
    data = requests.post(f"{settings.checker_api}/contest", json=payload, timeout=60).json()
    save(data, loop)

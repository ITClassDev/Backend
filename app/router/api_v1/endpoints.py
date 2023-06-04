from fastapi import APIRouter

from app.users.api import router as users_router
from app.auth.api import router as auth_router


api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (users_router, "users", "users"),
    (auth_router, "auth", "auth"),
   
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")
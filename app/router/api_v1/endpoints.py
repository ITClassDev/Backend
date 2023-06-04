from fastapi import APIRouter

from app.users.api import router as users_router
from app.auth.api import router as auth_router
from app.groups.api import router as groups_router
from app.achievements.api import router as achievements_router
from app.oauth.api import router as oauth_router


api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (users_router, "users", "users"),
    (auth_router, "auth", "auth"),
    (groups_router, "groups", "groups"),
    (achievements_router, "achievements", "achievements"),
    (oauth_router, "oauth", "oauth")

)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")

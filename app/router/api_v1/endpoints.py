from fastapi import APIRouter

from app.users.api import router as users_router
from app.auth.api import router as auth_router
from app.groups.api import router as groups_router
from app.achievements.api import router as achievements_router
from app.oauth.api import router as oauth_router
from app.notifications.api import router as notifications_router
from app.events.api import router as events_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (users_router, "users", "users"),
    (auth_router, "auth", "auth"),
    (groups_router, "groups", "groups"),
    (achievements_router, "achievements", "achievements"),
    (oauth_router, "oauth", "oauth"),
    (notifications_router, "notifications", "notifications"),
    (events_router, "events", "events")

)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")

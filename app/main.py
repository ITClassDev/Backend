import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from app import settings
from app.core.models import HealthCheck, JWTSettings
from app.router.api_v1.endpoints import api_router
from fastapi.openapi.utils import get_openapi
import app.sql_admin as sql_admin
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/storage", StaticFiles(directory=settings.user_storage),
          name="storage")  # User data storage(local)
sql_admin.create(app, settings.secret_key)
logging.basicConfig(filename="./app/logs/events.txt",
                    filemode='a',
                    format='%(asctime)s.%(msecs)d %(service_name)s %(levelname)s %(message)s; By: %(by_user)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logging.info("ShTP REST API Started", extra={"service_name": "main", "by_user": "root"})

@AuthJWT.load_config  # type: ignore
def get_config():
    # print("Seconds:", settings.jwt_access_token_expire_at_minutes * 60)
    return JWTSettings(authjwt_secret_key=settings.secret_key, authjwt_access_token_expires=settings.jwt_access_token_expire_at_minutes * 60)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,  # type: ignore
        content={"detail": exc.message}  # type: ignore
    )


@app.get("/", response_model=HealthCheck, tags=["status"])
async def health_check():
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description
    }


app.include_router(api_router, prefix=settings.api_v1_prefix)


# Add JWT for fastapi_jwt_auth in swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.project_name,
        version=settings.version,
        description=settings.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {"bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }}

    openapi_schema["security"] = [{"bearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)

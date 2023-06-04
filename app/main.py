import uvicorn
from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from app import settings
from app.core.models import HealthCheck, JWTSettings
from app.router.api_v1.endpoints import api_router
from fastapi.openapi.utils import get_openapi
import app.sql_admin as sql_admin

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug
)
sql_admin.create(app, settings.secret_key)




@AuthJWT.load_config  # type: ignore
def get_config():
    return JWTSettings(authjwt_secret_key=settings.secret_key)


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

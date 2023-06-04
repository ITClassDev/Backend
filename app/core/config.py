from pydantic import BaseSettings


class Settings(BaseSettings):
    # Base
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str

    # Database
    db_async_connection_str: str
    db_async_test_connection_str: str

    # JWT
    secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_at_minutes: int

    # Storage
    user_storage: str

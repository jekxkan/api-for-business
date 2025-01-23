from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    sqlalchemy_database_url: str = (
        "postgresql+asyncpg://user:zxcvb@localhost:5432/users_info"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
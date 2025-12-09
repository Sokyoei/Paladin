from functools import lru_cache

from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False

    # from pydantic import MySQLDsn

    # SQLALCHEMY_DATABASE_URL: MySQLDsn = "mysql+aiomysql://root:ahri@localhost:3306/paladin?charset=utf8mb4"
    # from pydantic import PostgresDsn

    # SQLALCHEMY_DATABASE_URL: PostgresDsn = "postgresql+asyncpg://root:ahri@localhost:5432/paladin"
    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:///./paladin.sqlite3"

    REDIS_URL: RedisDsn = "redis://localhost"

    JWT_SECRET_KEY: str = "U9oiu812ix1bqi9hap01h2nxn1j212mik"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    JWT_ALGORITHM: str = "HS256"

    FIRST_UID: int = 100000

    class Config:
        env_file = ".env", ".env.dev", ".env.prod"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

DEBUG = settings.DEBUG

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

REDIS_URL = settings.REDIS_URL

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
JWT_ALGORITHM = settings.JWT_ALGORITHM

FIRST_UID = settings.FIRST_UID

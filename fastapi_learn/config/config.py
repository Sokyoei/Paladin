from functools import lru_cache

from pydantic import MySQLDsn, PostgresDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi_learn import FASTAPILEARN_ROOT


class Settings(BaseSettings):
    DEBUG: bool = False

    # Flags
    USE_FASTAPI_USERS: bool = False

    # SQLite
    SQLALCHEMY_DATABASE_URI_SQLITE: str = "sqlite+aiosqlite:///./paladin.sqlite3"

    # PostgreSQL
    POSTGRESQL_HOST: str = "127.0.0.1"
    POSTGRESQL_PORT: int = 5432
    POSTGRESQL_USERNAME: str = "username"
    POSTGRESQL_PASSWORD: str = "password"
    POSTGRESQL_DB: str = "database"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI_POSTGRESQL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRESQL_USERNAME,
            password=self.POSTGRESQL_PASSWORD,
            host=self.POSTGRESQL_HOST,
            port=self.POSTGRESQL_PORT,
            path=self.POSTGRESQL_DB,
        )

    # MySQL
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_USERNAME: str = "username"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DB: str = "database"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI_MYSQL(self) -> MySQLDsn:
        return MySQLDsn.build(
            scheme="mysql+aiomysql",
            username=self.MYSQL_USERNAME,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            path=self.MYSQL_DB,
            query="charset=utf8mb4",
        )

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str | None = None
    REDIS_PASSWORD: str | None = None

    @computed_field
    @property
    def REDIS_URI(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USERNAME,
            password=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=None,
            query=None,
        )

    JWT_SECRET_KEY: str = "secret"  # use `os.urandom(24).hex()` to generate a key
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    JWT_ALGORITHM: str = "HS256"

    FIRST_UID: int = 100000

    model_config = SettingsConfigDict(
        env_file=[
            FASTAPILEARN_ROOT / "fastapi_learn/.env",
            FASTAPILEARN_ROOT / "fastapi_learn/.env.dev",
            FASTAPILEARN_ROOT / "fastapi_learn/.env.prod",
        ],
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

DEBUG = settings.DEBUG

SQLALCHEMY_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI_SQLITE

REDIS_URI = settings.REDIS_URI

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
JWT_ALGORITHM = settings.JWT_ALGORITHM

FIRST_UID = settings.FIRST_UID

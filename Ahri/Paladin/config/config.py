"""
config form envioronment variables and .env file
"""

from functools import lru_cache
from pathlib import Path

from pydantic import MySQLDsn, PostgresDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from Ahri.Paladin import PALADIN_ROOT


class Settings(BaseSettings):
    DEBUG: bool = False

    # dir
    LOG_DIR: Path = PALADIN_ROOT / "logs"
    DOWNLOAD_DIR: Path = PALADIN_ROOT / "downloads"

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

    # Minio
    MINIO_BUCKET_NAME: str = "paladin"
    MINIO_ENDPOINT: str = "127.0.0.1:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"

    # Nacos
    NACOS_IP: str = "127.0.0.1"
    NACOS_PORT: int = 8848

    @computed_field
    @property
    def NACOS_SERVER_ADDRESSES(self) -> str:
        return f"{self.NACOS_IP}:{self.NACOS_PORT}"

    NACOS_NAMESPACE: str = "public"
    NACOS_SERVICE_NAME: str = "paladin"
    NACOS_REGISTER_IP: str = "127.0.0.1"
    NACOS_REGISTER_PORT: int = 8000
    NACOS_GROUP: str = "DEFAULT_GROUP"
    NACOS_USERNAME: str = "nacos"
    NACOS_PASSWORD: str = "nacos"
    NACOS_DATA_ID: str = "paladin"

    model_config = SettingsConfigDict(
        env_file=[PALADIN_ROOT / ".env", PALADIN_ROOT / ".env.dev", PALADIN_ROOT / ".env.prod"],
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

DEBUG = settings.DEBUG

# dir
LOG_DIR = settings.LOG_DIR
DOWNLOAD_DIR = settings.DOWNLOAD_DIR

# Minio
MINIO_BUCKET_NAME = settings.MINIO_BUCKET_NAME
MINIO_ENDPOINT = settings.MINIO_ENDPOINT
MINIO_ACCESS_KEY = settings.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = settings.MINIO_SECRET_KEY

# SQLAlchemy URI
SQLALCHEMY_DATABASE_URI = str(settings.SQLALCHEMY_DATABASE_URI_POSTGRESQL)

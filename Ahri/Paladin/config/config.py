"""
config form envioronment variables and .env file
"""

from functools import lru_cache
from pathlib import Path

from pydantic import MySQLDsn, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from Ahri.Paladin import PALADIN_ROOT


class Settings(BaseSettings):
    DEBUG: bool = False

    # dir
    LOG_DIR: Path = PALADIN_ROOT / "logs"
    DOWNLOAD_DIR: Path = PALADIN_ROOT / "downloads"

    # PostgreSQL
    POSTGRESQL_HOST: str = "127.0.0.1"
    POSTGRESQL_PORT: int = 5432
    POSTGRESQL_USERNAME: str = "user"
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
    MYSQL_USERNAME: str = "user"
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

    # Minio
    MINIO_BUCKET_NAME: str = "paladin"
    MINIO_ENDPOINT: str = "127.0.0.1:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"

    model_config = SettingsConfigDict(
        env_file=[PALADIN_ROOT / ".env", PALADIN_ROOT / ".env.dev", PALADIN_ROOT / ".env.prod"],
        env_file_encoding="utf-8",
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

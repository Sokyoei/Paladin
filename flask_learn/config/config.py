from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./paladin.db"
    SECRET_KEY: str = "paladin"
    FIRST_UID: int = 100_0000

    model_config = SettingsConfigDict(env_file=[".env", ".env.dev", ".env.prod"], env_file_encoding="utf-8")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

SQLALCHEMY_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI
SECRET_KEY = settings.SECRET_KEY
FIRST_UID = settings.FIRST_UID

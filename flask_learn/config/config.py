from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from flask_learn import FLASKLEARN_ROOT


class Settings(BaseSettings):
    DEBUG: bool = False

    # SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./paladin.sqlite3"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./paladin.sqlite3"

    SECRET_KEY: str = "paladin"  # use `os.urandom(24).hex()` to generate a new key
    FIRST_UID: int = 100_0000

    FLASK_ADMIN_NAME: str = "Flask Learn Admin"

    model_config = SettingsConfigDict(
        env_file=[FLASKLEARN_ROOT / ".env", FLASKLEARN_ROOT / ".env.dev", FLASKLEARN_ROOT / ".env.prod"],
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

DEBUG = settings.DEBUG

SQLALCHEMY_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI
SECRET_KEY = settings.SECRET_KEY
FIRST_UID = settings.FIRST_UID

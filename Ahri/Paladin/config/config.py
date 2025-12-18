from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from Ahri.Paladin import PALADIN_ROOT


class Settings(BaseSettings):
    DEBUG: bool = False

    LOG_DIR: Path = PALADIN_ROOT / "logs"
    DOWNLOAD_DIR: Path = PALADIN_ROOT / "downloads"

    model_config = SettingsConfigDict(
        env_file=[PALADIN_ROOT / ".env", PALADIN_ROOT / ".env.dev", PALADIN_ROOT / ".env.prod"],
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

DEBUG = settings.DEBUG
LOG_DIR = settings.LOG_DIR
DOWNLOAD_DIR = settings.DOWNLOAD_DIR

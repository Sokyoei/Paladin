"""
配置
"""

from .config import DEBUG, DOWNLOAD_DIR, LOG_DIR, settings

settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
settings.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

__all__ = ["DEBUG", "DOWNLOAD_DIR", "LOG_DIR", "settings"]

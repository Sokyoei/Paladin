"""
配置
"""

from Ahri.Paladin import PALADIN_ROOT

LOG_DIR = PALADIN_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOAD_DIR = PALADIN_ROOT / "downloads"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

__all__ = ["DOWNLOAD_DIR", "LOG_DIR"]

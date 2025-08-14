"""
配置
"""

from Ahri.Paladin import PALADIN_ROOT

LOG_DIR = PALADIN_ROOT / "logs"
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

__all__ = ["LOG_DIR"]

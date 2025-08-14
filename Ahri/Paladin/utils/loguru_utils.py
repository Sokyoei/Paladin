import sys
from pathlib import Path

from loguru import logger

from Ahri.Paladin.config import LOG_DIR

FORMATTER = (
    "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>][<cyan>{file.path}:{line}</cyan>]"
    "[<level>{level}</level>]: <level>{message}</level>"
)


def init_logging(log_path: Path = LOG_DIR / "Paladin_{time:YYYY-MM-DD}.log"):
    logger.remove(handler_id=None)
    logger.add(sys.stderr, format=FORMATTER, colorize=True)
    logger.add(
        log_path,
        format=FORMATTER,
        rotation="00:00",
        retention="30 days",
        # compression="zip",
        enqueue=True,
    )

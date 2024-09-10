import sys

from loguru import logger

from Paladin.config import LOG_DIR


def init_logging():
    FORMATTER = (
        "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>][<cyan>{file}</cyan>][line:<cyan>{line}</cyan>]"
        "[<level>{level}</level>]: <level>{message}</level>"
    )

    logger.remove(handler_id=None)
    logger.add(sys.stderr, format=FORMATTER, colorize=True)
    logger.add(
        LOG_DIR / "Paladin_{time:YYYY-MM-DD}.log",
        format=FORMATTER,
        rotation="00:00",
        retention="30 days",
        # compression="zip",
        enqueue=True,
    )

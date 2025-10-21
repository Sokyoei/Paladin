from loguru import logger

from Ahri.Paladin.utils import init_logging


def main():
    init_logging()

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.success("success")
    logger.critical("critical")
    # logger.exception("exception")


if __name__ == "__main__":
    main()

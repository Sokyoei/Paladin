import logging

try:
    import loguru

    del loguru
except ModuleNotFoundError:
    pass

from Paladin.utils import init_logging


def main():
    init_logging()

    log = logging.getLogger()

    log.debug("debug")
    log.info("info")
    log.warning("warning")
    log.error("error")
    log.fatal("fatal")


if __name__ == "__main__":
    main()

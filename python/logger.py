import logging
import logging.handlers

formater = "[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s]: %(message)s"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("tempCodeRunnerFile.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(formater))

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(logging.Formatter(formater))

logger.addHandler(fh)
logger.addHandler(sh)

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")

# logging.basicConfig(filename="tempCodeRunnerFile.log", format=formater, level=logging.DEBUG, encoding="utf8")
# logging.handlers.TimedRotatingFileHandler()
# logging.warning("warning")
# logging.error("error")
# logging.info("info")
# logging.debug("debug")
# logging.critical("critical")

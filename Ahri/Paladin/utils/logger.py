"""
日志管理
"""

import logging
import logging.handlers

from Ahri.Paladin.config import LOG_DIR


class Logger(object):

    def __init__(self, log_name: str, level: int = logging.INFO) -> None:
        self.log_name = log_name
        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        self.formatter = logging.Formatter("[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s]: %(message)s")

        # 时间轮换
        th = logging.handlers.TimedRotatingFileHandler(self.log_name, backupCount=7)
        th.setFormatter(self.formatter)
        th.setLevel(level)
        self.logger.addHandler(th)

        # 终端显示
        sh = logging.StreamHandler()
        sh.setFormatter(self.formatter)
        sh.setLevel(logging.WARNING)
        self.logger.addHandler(sh)


log = Logger(LOG_DIR / "Paladin.log", logging.INFO).logger

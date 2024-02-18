"""
日志管理
"""

import logging
import logging.handlers


class Logger(object):

    def __init__(self) -> None:
        self.logger = logging.getLogger()
        self.formater = logging.Formatter("[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s]: %(message)s")

        # 时间轮换
        th = logging.handlers.TimedRotatingFileHandler("Paladin.log")
        th.setFormatter(self.formater)
        self.logger.addHandler(th)


log = Logger().logger

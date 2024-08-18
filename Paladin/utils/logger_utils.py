"""
日志
"""

from __future__ import annotations

import logging.config
from logging import LogRecord
from pathlib import Path

import yaml

from Paladin import PALADIN_ROOT


def init_logging(config_path: Path = PALADIN_ROOT / "Paladin/utils/logger.yaml"):
    with open(config_path) as f:
        config = yaml.load(f.read(), yaml.FullLoader)
        logging.config.dictConfig(config)


class PaladinFilter(logging.Filter):
    """
    PaladinFilter
    """

    def __init__(self, name: str = "") -> None:
        super().__init__(name)

    def filter(self, record: LogRecord) -> bool | LogRecord:
        return super().filter(record)

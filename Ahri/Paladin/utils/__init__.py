from Ahri.Paladin.check import check_package_installed

from .check import check_path
from .decorator import async_timer, timer
from .logger import log

if check_package_installed("loguru"):
    from .loguru_utils import init_logging
else:
    from .logger_utils import init_logging

__all__ = ["async_timer", "check_path", "init_logging", "log", "timer"]

if check_package_installed("requests") and check_package_installed("tqdm"):
    from .decorator import download
    from .download import download_file

    __all__ += ["download", "download_file"]

if check_package_installed("paho"):
    from .mqtt_utils import ClientMode, MQTTClient

    __all__ += ["ClientMode", "MQTTClient"]

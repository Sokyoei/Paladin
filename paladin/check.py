import importlib.util

from loguru import logger


def check_module_installed(module_name: str) -> bool:
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return False
    else:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        logger.info(f"{module} {module.__version__} is installed")
        return True


def check_package_installed(package_name: str) -> bool:
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        return True
    else:
        logger.warning(f"{package_name} is not installed, will ignore this package.")
        return False

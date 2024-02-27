"""
检查
"""

import os
from pathlib import Path
from typing import Union


def check_path(path: Union[Path, str]):
    if isinstance(path, Path):
        if not path.exists():
            print("path not exists")
        else:
            return path
    else:
        if not os.path.exists(path):
            print("path not exists")
        else:
            return path

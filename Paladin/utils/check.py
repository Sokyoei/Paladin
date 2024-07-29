"""
检查
"""

from __future__ import annotations

import os
from pathlib import Path


def check_path(path: str | os.PathLike) -> bool:
    if isinstance(path, Path):
        return path.exists()
    elif isinstance(path, str):
        return os.path.exists(path)
    else:
        raise NotImplementedError(f"{type(path)} are not supported.")


def check_path_and_mkdir(path: Path):
    if not path.exists():
        path.mkdir(parents=True)

from __future__ import annotations

import os
import time
from functools import wraps
from typing import Optional

from Paladin.utils import download_file


def timer(func):
    """统计函数的执行时间

    Examples:
    >>> @timer
    ... def add(a, b):
    ...     return a + b

    >>> add(1, 2)  # doctest: +ELLIPSIS
    add: ...s
    3
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        ret = func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f"{func.__name__}: {t2 - t1}s")

        return ret

    return wrapper


def async_timer(func):
    """统计异步函数的执行时间

    Examples:
    >>> import asyncio

    >>> @async_timer
    ... async def add(a, b):
    ...     await asyncio.sleep(3)
    ...     return a + b

    >>> asyncio.run(add(1, 2))  # doctest: +ELLIPSIS
    add: ...s
    3
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        ret = await func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f"{func.__name__}: {t2 - t1}s")

        return ret

    return wrapper


def download(url: str, dst_path: Optional[str | os.PathLike] = None, check_exists: bool = True):
    """下载文件装饰器

    See also:
        .download.download_file()
    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            download_file(url, dst_path, check_exists)
            ret = func(*args, **kwargs)
            return ret

        return inner

    return wrapper

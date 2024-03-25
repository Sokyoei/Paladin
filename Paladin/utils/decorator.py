import time
from functools import wraps


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

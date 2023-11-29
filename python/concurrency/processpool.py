"""
Python 进程池
"""

import time
from concurrent.futures import ProcessPoolExecutor, as_completed


def do_work(n):
    time.sleep(n)
    print(f"do work: sleep {n}")


if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=16) as pp:
        task1 = pp.submit(do_work, 1)
        task2 = pp.submit(do_work, 2)
        task3 = pp.submit(do_work, 3)

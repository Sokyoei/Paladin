"""
Python 进程池
"""

import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor, as_completed


def do_work(n) -> None:
    time.sleep(n)
    print(f"do work: sleep {n}")


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=16) as pp:
        task1 = pp.submit(do_work, 1)
        task2 = pp.submit(do_work, 2)
        task3 = pp.submit(do_work, 3)

    with mp.Pool(3) as p:
        print(p.map(do_work, [1, 2, 3]))

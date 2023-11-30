"""
Python 线程池
"""

import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed


def do_work(n):
    time.sleep(n)
    print(f"do work: sleep {n}")
    return n


def do_finish(task: Future):
    if task.done():
        print(f"{task} finish")


args = [1, 2, 3]

with ThreadPoolExecutor(max_workers=16) as tp:
    # generator
    tasks = tp.map(do_work, args)
    for i in tasks:
        print(i)
    # iterator
    tasks = [tp.submit(do_work, arg) for arg in args]
    for future in as_completed(tasks):
        print(future.result())

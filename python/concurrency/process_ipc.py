# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     notebook_metadata_filter: -all,jupytext
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
# ---

# %% [markdown]
"""
# IPC 进程间通信
"""

# %%
import logging
import multiprocessing as mp
import sys
import time
from multiprocessing.connection import Connection
from multiprocessing.queues import JoinableQueue, Queue, SimpleQueue
from multiprocessing.shared_memory import SharedMemory
from multiprocessing.sharedctypes import Synchronized, SynchronizedArray
from multiprocessing.synchronize import Lock

from loguru import logger

from paladin.config import settings

# %% [markdown]
# ## 消息传递
#
# [Pipe](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Pipe)/
# [Queue](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Queue)/
# [SimpleQueue](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.SimpleQueue)/
# [JoinableQueue](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Pipe)
# , 底层是管道，数据需要 pickle 序列化后传递，拷贝数据。


# %%
def queue_worker(q: Queue | SimpleQueue) -> None:
    while True:
        item = q.get()
        if item is None:
            break
        logger.info(f"{item=}")
        time.sleep(0.1)
    logger.info("queue worker 退出")


def mp_Queue_example() -> None:
    logger.debug("mp.Queue")
    q = mp.Queue()
    p = mp.Process(target=queue_worker, args=(q,))
    p.start()

    for i in range(10):
        q.put(i)
    q.put(None)  # 发送哨兵
    p.join()


def mp_SimpleQueue_example() -> None:
    logger.debug("mp.SimpleQueue")
    q = mp.SimpleQueue()
    p = mp.Process(target=queue_worker, args=(q,))
    p.start()

    for i in range(10):
        q.put(i)
    q.put(None)
    p.join()


# %%
def joinable_queue_worker(q: JoinableQueue) -> None:
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break
        logger.info(f"{item=}")
        time.sleep(0.1)
        q.task_done()
    logger.info("joinable queue worker 退出")


def mp_JoinableQueue_example() -> None:
    logger.debug("mp.JoinableQueue")
    q = mp.JoinableQueue()
    p = mp.Process(target=joinable_queue_worker, args=(q,))
    p.daemon = True
    p.start()

    for i in range(10):
        q.put(i)

    q.put(None)
    q.join()
    logger.info(f"{'All tasks done.'}")


# %%
def pipe_worker(conn: Connection):
    while True:
        item = conn.recv()
        if item is None:
            break
        logger.info(f"子进程收到：{item=}")
        conn.send(f"子进程发送：{item=}")
    conn.close()


def mp_Pipe_example() -> None:
    parent_conn, child_conn = mp.Pipe()
    p = mp.Process(target=pipe_worker, args=(child_conn,))
    p.start()

    for i in range(10):
        parent_conn.send(i)
        logger.info(f"父进程收到回复：{parent_conn.recv()}")

    parent_conn.send(None)
    p.join()
    parent_conn.close()


# %% [markdown]
# ## 共享内存
#
# [SharedMemory](https://docs.python.org/zh-cn/3/library/multiprocessing.shared_memory.html#multiprocessing.shared_memory.SharedMemory)/
# [Array](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Array)/
# [Value](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Value)/
# [RawArray](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.sharedctypes.RawArray)/
# [RawValue](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.sharedctypes.RawValue)
# , 进程间是同一块物理内存，不拷贝，需要处理并发竞争。


# %%
def shm_worker(shm_name: str, shm_size: int, lock: Lock):
    # 子进程是挂载端，传入的 size 参数被 Python 忽略，shm.buf 是完整的 OS 内存页大小。
    shm = SharedMemory(name=shm_name, size=shm_size)
    try:
        buf = shm.buf
        if buf is None:
            raise RuntimeError("SharedMemory buffer is None")
        logger.info(f"子进程操作系统分配的内存页大小：{len(buf)=}字节")

        with lock:
            for i in range(10):
                buf[i] += 10
        # logger.info(f"子进程修改完成，{list(buf[:shm.size])=}")
        logger.info(f"子进程修改完成，{list(buf[:shm_size])=}")
    finally:
        shm.close()


def mp_SharedMemory_example() -> None:
    logger.debug("mp.shared_memory.SharedMemory")
    # 父进程是创建端，底层 OS 分配的是完整的内存页，但是 shm.buf 的 memoryview 视图被 Python 限制为申请的 size.
    shm = SharedMemory(create=True, size=10)
    try:
        buf = shm.buf
        if buf is None:
            raise RuntimeError("SharedMemory buffer is None")
        logger.info(f"父进程操作系统分配的内存页大小：{len(buf)=}字节")

        buf[:5] = bytearray([1, 2, 3, 4, 5])
        logger.info(f"初始数据：{list(buf[:shm.size])=}")

        lock = mp.Lock()
        p = mp.Process(target=shm_worker, args=(shm.name, shm.size, lock))
        p.start()
        p.join()

        logger.info(f"父进程读取结果：{list(buf[:shm.size])=}")
    finally:
        shm.close()
        shm.unlink()


# %%
def value_array_worker(
    val: Synchronized, arr: SynchronizedArray, raw_val: Synchronized, raw_arr: SynchronizedArray, lock: Lock
):
    # mp.Value/mp.Array 带锁，安全。
    val.value = 10
    arr[:] = [i + 10 for i in arr]
    # mp.RawValue/mp.RawArray 不带锁，必须使用 lock 保护。
    with lock:
        raw_val.value += 10
    with lock:
        raw_arr[:] = [i + 10 for i in raw_arr]


def mp_Value_Array_example():
    logger.debug("mp.Value/mp.Array/mp.RawValue/mp.RawArray")
    val = mp.Value('i', 1)
    raw_val = mp.RawValue('i', 1)
    arr = mp.Array('i', [1, 2, 3])
    raw_arr = mp.RawArray('i', [1, 2, 3])
    lock = mp.Lock()

    logger.info(f"父进程：{val=}, {raw_val=}, {arr[:]=}, {raw_arr[:]=}")

    p = mp.Process(target=value_array_worker, args=(val, arr, raw_val, raw_arr, lock))
    p.start()
    logger.info(f"子进程执行时父进程：{val=}, {raw_val=}, {arr[:]=}, {raw_arr[:]=}")

    p.join()
    logger.info(f"子进程执行结束后父进程：{val=}, {raw_val=}, {arr[:]=}, {raw_arr[:]=}")


# %%
def main():
    mp_Queue_example()
    mp_SimpleQueue_example()
    mp_JoinableQueue_example()
    mp_Pipe_example()

    if sys.version_info >= (3, 7):  # noqa: UP036
        mp_SharedMemory_example()

    mp_Value_Array_example()


if __name__ == '__main__':
    if settings.DEBUG:
        mp_logger = mp.log_to_stderr(logging.DEBUG)
        mp_logger.info("multiprocessing debug log enabled.")

    main()

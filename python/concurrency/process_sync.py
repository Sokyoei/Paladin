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
# # Synchronization 进程间同步

# %%
import multiprocessing as mp
import time
from multiprocessing.synchronize import Barrier, BoundedSemaphore, Condition, Event, Lock, RLock, Semaphore

from loguru import logger

# %% [markdown]
# ## [Lock](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Lock) 互斥锁


# %%
def lock_worker(lock: Lock, idx: int):
    with lock:
        logger.info(f"Lock 临界区 进程{idx} 进入")
        time.sleep(0.1)
        logger.info(f"Lock 临界区 进程{idx} 退出")


def mp_Lock_example():
    logger.debug("mp.Lock 互斥锁")
    lock = mp.Lock()
    proc_list: list[mp.Process] = []
    for i in range(5):
        p = mp.Process(target=lock_worker, args=(lock, i))
        proc_list.append(p)
        p.start()
    for p in proc_list:
        p.join()


# %% [markdown]
# ## [RLock](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.RLock) 可重入锁


# %%
def rlock_worker(rlock: RLock, idx: int):
    rlock.acquire()
    logger.info(f"RLock 临界区 进程{idx} 进入")
    rlock.acquire()
    logger.info(f"RLock 临界区 进程{idx} 进入")
    time.sleep(1)
    rlock.release()
    logger.info(f"RLock 临界区 进程{idx} 退出")
    rlock.release()
    logger.info(f"RLock 临界区 进程{idx} 退出")


def mp_RLock_example():
    logger.debug("mp.RLock 可重入锁")
    rlock = mp.RLock()
    proc_list: list[mp.Process] = []
    for i in range(3):
        p = mp.Process(target=rlock_worker, args=(rlock, i))
        proc_list.append(p)
        p.start()
    for p in proc_list:
        p.join()


# %% [markdown]
# ## [Event](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Event) 事件信号


# %%
def event_worker(evt: Event, idx: int):
    logger.info(f"Event 进程{idx} 等待信号")
    evt.wait()
    logger.info(f"Event 进程{idx} 收到信号，继续执行")


def mp_Event_example():
    logger.debug("mp.Event 事件信号")
    event = mp.Event()
    proc_list: list[mp.Process] = []
    for i in range(3):
        p = mp.Process(target=event_worker, args=(event, i))
        proc_list.append(p)
        p.start()
    time.sleep(1)
    logger.info("主进程发送 Event 信号")
    event.set()
    for p in proc_list:
        p.join()


# %% [markdown]
# ## [Condition](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Condition) 条件变量


# %%
def cond_consumer(cond: Condition):
    with cond:
        logger.info("Condition 消费者等待通知")
        cond.wait()
        logger.info("Condition 消费者收到通知")


def cond_producer(cond: Condition):
    time.sleep(1)
    with cond:
        logger.info("Condition 生产者发送 notify")
        cond.notify()


def mp_Condition_example():
    logger.debug("mp.Condition 条件变量")
    cond = mp.Condition()
    consumer = mp.Process(target=cond_consumer, args=(cond,))
    producer = mp.Process(target=cond_producer, args=(cond,))
    consumer.start()
    producer.start()
    consumer.join()
    producer.join()


# %% [markdown]
# ## [Semaphore](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Semaphore) / BoundedSemaphore 信号量
# BoundedSemaphore 对比 Semaphore 增加了计数校验，release 次数不能大于初始值。


# %%
def sem_worker(sem: Semaphore, idx: int):
    with sem:
        logger.info(f"Semaphore 进程{idx} 进入临界区")
        time.sleep(1)
        logger.info(f"Semaphore 进程{idx} 离开临界区")


def mp_Semaphore_example():
    logger.debug("mp.Semaphore 信号量")
    sem = mp.Semaphore(2)
    proc_list: list[mp.Process] = []
    for i in range(5):
        p = mp.Process(target=sem_worker, args=(sem, i))
        proc_list.append(p)
        p.start()
    for p in proc_list:
        p.join()


def bsem_worker(bsem: BoundedSemaphore, idx: int):
    bsem.acquire()
    logger.info(f"BoundedSemaphore 进程{idx} 进入临界区")
    bsem.release()
    logger.info(f"BoundedSemaphore 进程{idx} 离开临界区")
    try:
        bsem.release()
    except ValueError as e:
        logger.info(f"BoundedSemaphore 越界: {e}")


def mp_BoundedSemaphore_example():
    logger.debug("mp.BoundedSemaphore 有界信号量")
    bsem = mp.BoundedSemaphore(2)
    proc_list: list[mp.Process] = []
    for i in range(5):
        p = mp.Process(target=bsem_worker, args=(bsem, i))
        proc_list.append(p)
        p.start()
    for p in proc_list:
        p.join()


# %% [markdown]
# ## [Barrier](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.Barrier) 屏障


# %%
def barrier_worker(barr: Barrier, idx: int):
    time.sleep(1 * idx)
    logger.info(f"Barrier 进程{idx} 到达屏障点，等待其他进程")
    barr.wait()
    logger.info(f"Barrier 进程{idx} 全部就位，一起放行！")


def mp_Barrier_example():
    logger.debug("mp.Barrier 屏障")
    barr = mp.Barrier(3)
    proc_list = []
    for i in range(3):
        p = mp.Process(target=barrier_worker, args=(barr, i))
        proc_list.append(p)
        p.start()
    for p in proc_list:
        p.join()


# %%
def main():
    mp_Lock_example()
    mp_RLock_example()
    mp_Event_example()
    mp_Condition_example()
    mp_Semaphore_example()
    mp_BoundedSemaphore_example()
    mp_Barrier_example()


if __name__ == '__main__':
    main()

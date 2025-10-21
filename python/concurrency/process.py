import multiprocessing as mp
import os
import time

from loguru import logger

cond = mp.Condition()
lock = mp.Lock()
rlock = mp.RLock()
barr = mp.Barrier(3)
sem = mp.Semaphore()
sem = mp.BoundedSemaphore()
event = mp.Event()


def do_work(x: int) -> None:
    logger.info(f"{os.getpid()=}")
    logger.info(f"{x=}")
    return x * x


def mp_Process_example() -> None:
    p1 = mp.Process(target=do_work, args=(2,))
    p2 = mp.Process(target=do_work, args=(3,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()


def mp_Pool_example() -> None:
    with mp.Pool(processes=8) as pool:
        # apply 执行单个任务
        print(f"{' mp.Pool().apply() ':-^120}")
        result_apply = pool.apply(do_work, args=(4,))
        logger.info(f"{result_apply=}")

        print(f"{' mp.Pool().apply_async() ':-^120}")
        result_apply_async = pool.apply_async(do_work, args=(5,))
        logger.info(f"{result_apply_async.ready()=}")
        logger.info(f"{result_apply_async.get()=}")

        # map 批量执行任务
        print(f"{' mp.Pool().map() ':-^120}")
        result_map = pool.map(do_work, range(16))
        logger.info(f"{result_map=}")

        print(f"{' mp.Pool().map_async() ':-^120}")
        result_map_async = pool.map_async(do_work, range(16))
        logger.info(f"{result_map_async.ready()=}")
        logger.info(f"{result_map_async.get()=}")

        # imap 迭代执行任务，内存友好
        print(f"{' mp.Pool().imap() ':-^120}")
        result_imap = pool.imap(do_work, range(16))
        for i in result_imap:
            logger.info(f"{i=}")

        print(f"{' mp.Pool().imap_unordered() ':-^120}")
        result_imap_unordered = pool.imap_unordered(do_work, range(16))
        for i in result_imap_unordered:
            logger.info(f"{i=}")

        # starmap 批量执行任务，参数为元组
        print(f"{' mp.Pool().starmap() ':-^120}")
        result_starmap = pool.starmap(do_work, [(6,), (7,), (8,)])
        logger.info(f"{result_starmap=}")

        print(f"{' mp.Pool().starmap_async() ':-^120}")
        result_starmap_async = pool.starmap_async(do_work, [(9,), (10,), (11,)])
        logger.info(f"{result_starmap_async.ready()=}")
        logger.info(f"{result_starmap_async.get()=}")


def queue_worker(q: mp.Queue) -> None:
    while True:
        item = q.get()
        if item is None:
            break
        logger.info(f"{item=}")
        time.sleep(1)


def mp_Queue_example() -> None:

    q = mp.Queue()
    p = mp.Process(target=queue_worker, args=(q,))
    p.start()

    for i in range(10):
        q.put(i)

    q.put(None)
    p.join()


def simple_queue_worker(q: mp.SimpleQueue) -> None:
    while True:
        if not q.empty():
            item = q.get()
            logger.info(f"{item=}")
            time.sleep(1)
        else:
            break


def mp_SimpleQueue_example() -> None:

    q = mp.SimpleQueue()
    p = mp.Process(target=simple_queue_worker, args=(q,))
    p.start()

    for i in range(10):
        q.put(i)

    time.sleep(2)
    p.join()


def joinable_queue_worker(q: mp.JoinableQueue) -> None:
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break
        logger.info(f"{item=}")
        time.sleep(1)
        q.task_done()


def mp_JoinableQueue_example() -> None:

    q = mp.JoinableQueue()
    p = mp.Process(target=joinable_queue_worker, args=(q,))
    p.daemon = True
    p.start()

    for i in range(10):
        q.put(i)

    q.put(None)
    q.join()
    logger.info(f"{'All tasks done.'}")


def mp_Pipe_example() -> None:
    pass


def mp_Value_example() -> None:
    pass


def mp_Array_example() -> None:
    pass


def main():
    logger.info(f"{mp.cpu_count()=}")  # == os.cpu_count()

    print(f"{' mp.Process() ':#^120}")
    mp_Process_example()
    print(f"{' mp.Pool() ':#^120}")
    mp_Pool_example()
    print(f"{' mp.Queue() ':#^120}")
    mp_Queue_example()
    print(f"{' mp.SimpleQueue() ':#^120}")
    mp_SimpleQueue_example()
    print(f"{' mp.JoinableQueue() ':#^120}")
    mp_JoinableQueue_example()
    print(f"{' mp.Pipe() ':#^120}")
    mp_Pipe_example()
    print(f"{' mp.Value() ':#^120}")
    mp_Value_example()
    print(f"{' mp.Array() ':#^120}")
    mp_Array_example()


if __name__ == "__main__":
    # NOTE:
    # Windows 下，子进程会重新导入主模块，因此需要将创建进程的代码放在 if __name__ == "__main__" 块中，
    # 否则会无限递归创建子进程
    main()

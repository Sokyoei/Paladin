import inspect
import threading
import time
from typing import List

lock = threading.Lock()  # 锁
rlock = threading.RLock()  # 递归锁
cond = threading.Condition()  # 条件变量
event = threading.Event()  # 事件锁
sem = threading.Semaphore(3)  # 信号量
bsem = threading.BoundedSemaphore(3)  # 带界信号量
barr = threading.Barrier(3)  # 屏障锁


########################################################################################################################
# Thread: Thread/Timer
########################################################################################################################
def do_work(args) -> None:
    print(args)


# 创建线程
# 方式一：线程直接执行函数
func_thread = threading.Thread(target=do_work, args=("func_thread: hello world",))
# 启动线程
func_thread.start()
# 等待线程结束，会阻塞当前线程
func_thread.join()


# 方式二：继承 threading.Thread 类，重写 run 方法
class DoWork(threading.Thread):
    def __init__(self, args) -> None:
        super().__init__()
        self.args = args

    def run(self) -> None:
        print(self.args)


class_thread = DoWork("class_thread: hello world")
class_thread.start()
class_thread.join()

func_timer = threading.Timer(3, function=do_work, args=("func_timer: hello world",))
func_timer.start()
func_timer.join()


########################################################################################################################
# Control: Lock/Condition
########################################################################################################################
cond_counter = 0
print(f"{'condition example':=^120}")


def odd_number_cond():
    global cond_counter, cond
    func_name = inspect.currentframe().f_code.co_name

    for _ in range(50):
        with cond:
            while cond_counter % 2 == 0:  # 如果是偶数，则等待
                cond.wait()
            print(f"{func_name}: {cond_counter}")
            cond_counter += 1
            cond.notify_all()


def even_number_cond():
    global cond_counter, cond
    func_name = inspect.currentframe().f_code.co_name

    for _ in range(50):
        with cond:
            while cond_counter % 2 == 1:  # 如果是奇数，则等待
                cond.wait()
            print(f"{func_name}: {cond_counter}")
            cond_counter += 1
            cond.notify_all()


odd_thread_cond = threading.Thread(target=odd_number_cond)
even_thread_cond = threading.Thread(target=even_number_cond)
odd_thread_cond.start()
even_thread_cond.start()
odd_thread_cond.join()
even_thread_cond.join()


########################################################################################################################
# Control: Semaphore/BoundedSemaphore
########################################################################################################################
# Semaphore ------------------------------------------------------------------------------------------------------------
print(f"{'Semaphore example':=^120}")


def sem_func(i):
    with sem:
        # sem.acquire()
        time.sleep(1)
        print(f"Semaphore worker {i} is working")
        # sem.release()


sem_threads: List[threading.Thread] = []
for i in range(9):
    sem_threads.append(threading.Thread(target=sem_func, args=(i,)))
    sem_threads[i].start()

for t in sem_threads:
    t.join()

# BoundedSemaphore-----------------------------------------------------------------------------------------------------
print(f"{'BoundedSemaphore example':=^120}")


def bsem_func(i):
    with bsem:
        time.sleep(1)
        print(f"BoundedSemaphore worker {i} is working")


bsem_threads: List[threading.Thread] = []
for i in range(10):
    bsem_threads.append(threading.Thread(target=bsem_func, args=(i,)))
    bsem_threads[i].start()

for t in bsem_threads:
    t.join()


########################################################################################################################
# Control: Event
########################################################################################################################
event_counter = 0
odd_event = threading.Event()
even_event = threading.Event()

print(f"{'Event example':=^120}")


def odd_number_event():
    global event_counter
    func_name = inspect.currentframe().f_code.co_name

    for _ in range(50):
        odd_event.wait()
        print(f"{func_name}: {event_counter}")
        event_counter += 1
        odd_event.clear()
        even_event.set()  # 通知偶数线程


def even_number_event():
    global event_counter
    func_name = inspect.currentframe().f_code.co_name

    for _ in range(50):
        even_event.wait()
        print(f"{func_name}: {event_counter}")
        event_counter += 1
        even_event.clear()
        odd_event.set()  # 通知奇数线程


# 初始让偶数线程先执行
even_event.set()

# 创建并启动线程
odd_thread_event = threading.Thread(target=odd_number_event)
even_thread_event = threading.Thread(target=even_number_event)
odd_thread_event.start()
even_thread_event.start()

# 等待线程结束
odd_thread_event.join()
even_thread_event.join()


########################################################################################################################
# Control: Barrier
########################################################################################################################
print(f"{'Barrier example':=^120}")


def barrier_action():
    print("All workers completed")


barrier = threading.Barrier(parties=3, action=barrier_action)


def barrier_worker(worker_id, barrier: threading.Barrier):
    print(f"Worker {worker_id} starting work")
    time.sleep(worker_id)  # 模拟不同的工作时间
    print(f"Worker {worker_id} finished work, waiting at barrier")

    # 等待所有线程到达屏障点
    barrier.wait()

    print(f"Worker {worker_id} passed the barrier and continuing")


# 创建并启动线程
barrier_threads: List[threading.Thread] = []
for i in range(3):
    t = threading.Thread(target=barrier_worker, args=(i, barrier))
    barrier_threads.append(t)
    t.start()

# 等待所有线程完成
for t in barrier_threads:
    t.join()

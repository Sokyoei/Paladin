import threading

lock = threading.Lock()  # 锁
rlock = threading.RLock()  # 递归锁
cond = threading.Condition()  # 条件变量
sem = threading.Semaphore(3)  # 信号量
event = threading.Event()  # 事件锁
barr = threading.Barrier(3)  # 屏障锁


def do_work(args) -> None:
    print(args)


func_thread = threading.Thread(target=do_work, args=("func_thread: hello world",))
func_thread.start()
func_thread.join()

func_timer = threading.Timer(3, function=do_work, args=("func_timer: hello world",))
func_timer.start()
func_timer.join()


class DoWork(threading.Thread):
    def __init__(self, args) -> None:
        super().__init__()
        self.args = args

    def run(self) -> None:
        print(self.args)


class_thread = DoWork("class_thread: hello world")
class_thread.start()

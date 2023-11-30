import multiprocessing as mp
import os


def do_work() -> None:
    print(f"{os.getpid()=}")


if __name__ == "__main__":
    p1 = mp.Process(target=do_work)
    p2 = mp.Process(target=do_work)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

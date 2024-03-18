"""
interrupt 中断
"""

import atexit
import os
import platform
import random
import signal
import time


@atexit.register
def atexit_kill():
    # todo something
    print("atexit killed")


def kill(a, b):
    # todo something
    print("signal killed")


def main():
    if platform.system() == "Windows":
        os.system("chcp 65001")

    pid = os.getpid()
    while True:
        n = random.random()
        print(f"{n=}")
        if n < 0.5:
            if platform.system() == "Linux":
                os.kill(pid, signal.SIGINT)
                time.sleep(10)
            elif platform.system() == "Windows":
                os.popen(f"taskkill.exe /F /pid:{pid}")
                time.sleep(10)
            else:
                raise RuntimeError


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, kill)
    signal.signal(signal.SIGINT, kill)
    main()

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
# # Process 进程

# %%
import logging
import multiprocessing as mp
import os

from loguru import logger

from paladin.config import settings


# %%
def do_worker(x: int):
    logger.info(f"do_work 进程 PID: {os.getpid()=}")
    logger.info(f"do_work 进程父 PID: {os.getppid()=}")
    logger.info(f"{x*x=}")


# %%
class HelloWorker(mp.Process):

    def __init__(self, arg):
        super().__init__(daemon=True)
        self.arg = arg

    def run(self) -> None:
        logger.info(f"HelloWorker 进程 PID: {os.getpid()=}")
        logger.info(f"HelloWorker 进程父 PID: {os.getppid()=}")
        logger.info(f"hello {self.arg}")


# %%
def main():
    logger.info(f"CPU 核心数：{mp.cpu_count()=}")
    logger.info(f"进程 PID: {os.getpid()=}")
    logger.info(f"进程父 PID: {os.getppid()=}")

    helloworker = HelloWorker("world")
    helloworker.start()

    doworker = mp.Process(target=do_worker, args=(2,))
    doworker.start()

    doworker.join()
    helloworker.join()  # 等待守护进程结束


# %%
if __name__ == "__main__":
    # NOTE:
    # Windows 下，子进程会重新导入主模块，因此需要将创建进程的代码放在 if __name__ == "__main__" 块中，
    # 否则会无限递归创建子进程
    if settings.DEBUG:
        mp_logger = mp.log_to_stderr(logging.DEBUG)
        mp_logger.info("multiprocessing debug log enabled.")

    main()

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
# # Manager 服务进程

# %%
import multiprocessing as mp
from multiprocessing.managers import BaseManager

from loguru import logger


# %%
def manager_worker(dict_: dict, list_: list):
    dict_[1] = "1"
    dict_["2"] = 2
    dict_[0.25] = None
    list_.reverse()


def mp_Manager_example() -> None:
    with mp.Manager() as manager:
        dict_ = manager.dict()
        list_ = manager.list(range(10))

        p = mp.Process(target=manager_worker, args=(dict_, list_))
        p.start()
        p.join()

        logger.info(f"manager dict: {dict_}")
        logger.info(f"manager list: {list_}")


# %%
class Math:

    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def mul(x, y):
        return x * y


class AhriManager(BaseManager):
    pass


AhriManager.register("Math", Math)


def AhriManager_example() -> None:
    with AhriManager() as am:
        math = am.Math()  # pyright: ignore[reportAttributeAccessIssue]
        logger.info(math.add(1, 2))
        logger.info(math.mul(1, 2))


# %%
def main():
    mp_Manager_example()
    AhriManager_example()


if __name__ == '__main__':
    main()

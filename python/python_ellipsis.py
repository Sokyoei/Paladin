# ellipsis ...

from random import shuffle
from typing import Callable, Tuple

import numpy as np

# <class 'ellipsis'>
print(type(...))
print(...)
print(bool(...))  # True
a = ...  # ... 可以为右值，不可以为左值

# numpy
x = np.arange(24).reshape((2, 3, 4))
print(x)
print(x[..., 0])
print(x[:, :, 0])


def func(): ...


def func2():
    NotImplemented


l = [1, 2, 3]  # noqa: E741
l.append(l)
print(l)  # [1, 2, 3, [...]]


# 类型提示中缺省未知类型或未知值
# 不确定返回的函数参数有几个，是哪些
def foo() -> Callable[..., int]:
    return lambda x: 1


# 不确定序列中其他元素的个数和类型
def foo2() -> Tuple[int, ...]:
    return 1, 2, 3


# 不确定初始值或默认值
def foo3(param: list = ...):
    return param


class MyList(list):
    def __init__(self, iterable):
        super().__init__()
        self._ = list(iterable)

    def __repr__(self):
        return self._.__repr__()

    def __getitem__(self, item):
        if item is ...:
            to_return = self._[:]
            shuffle(to_return)
            return to_return
        else:
            return self._.__getitem__(item)


# 得到一个 shuffle 后的列表，并保持原列表内容不变
m = MyList(i for i in range(10))
print(m[...])
print(m)

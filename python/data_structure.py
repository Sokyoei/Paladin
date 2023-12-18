"""
Python Data Structure
"""

import bisect
import enum
import heapq
from array import array
from collections import (
    ChainMap,
    Counter,
    OrderedDict,
    UserDict,
    UserList,
    UserString,
    defaultdict,
    deque,  # 双端队列
    namedtuple,
)
from queue import LifoQueue, PriorityQueue, Queue, SimpleQueue

########################################################################################################################
# list
########################################################################################################################
list()
list_ = [1]
UserList()

########################################################################################################################
# tuple
########################################################################################################################
tuple()
tuple_ = (1, "we", b"\n")
Point = namedtuple("Point", ["x", "y"])
p1 = Point(1, 2)

########################################################################################################################
# set
########################################################################################################################
set()
set_ = {1, "c"}
frozenset()

########################################################################################################################
# dict
# Python 3.7 起保留 dict 的插入顺序
########################################################################################################################
dict()
dict_ = {1: 2}
OrderedDict()
defaultdict()
UserDict()

########################################################################################################################
# binary
########################################################################################################################
bytes()  # 不可变
bytearray()  # 可变
# memoryview()  # 内存视图，需要支持缓冲区协议(bytes, bytearray)

Counter()
ChainMap()
# UserString()
deque()
# array()

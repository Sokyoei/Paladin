from ctypes import POINTER, Structure, c_char_p, c_int
from pathlib import Path
from typing import ClassVar, List, Tuple

import numpy as np

ctypes_example = np.ctypeslib.load_library("ctypes_example", Path(".").absolute())

# 2d array
arg = np.arange(9, dtype=c_int)
c_int_3x3_p = np.ctypeslib.ndpointer(dtype=c_int, ndim=2, shape=(3, 3))
# AhriC.array_add.argtypes = [c_int_3x3_p]
ctypes_example.array_add.restype = c_int_3x3_p
aa = np.ctypeslib.as_ctypes(arg)
ret = ctypes_example.array_add(aa)
print(np.ctypeslib.as_array(ret, shape=(3, 3)))


# struct
class Student(Structure):
    _fields_: ClassVar[List[Tuple]] = [("age", c_int), ("name", c_char_p)]


stus = (Student * 3)((1, "Ahri".encode()), (2, "Sokyoei".encode()), (3, "Nono".encode()))
# AhriC.student_add.argtypes = [POINTER(Student)]
ctypes_example.student_add.restype = POINTER(Student)
stus_ret = ctypes_example.student_add(stus)
for i in range(3):  # for i in stus_ret 会越界
    print(stus_ret[i].age, stus_ret[i].name)


# C struct 内指针变量，内存由 Python 端分配（Python 端传入数组，C 端指针接收）
NUM = 5


class Ahri(Structure):
    _fields_ = [("age", c_int), ("score", POINTER(c_int)), ("score_len", c_int)]


a = Ahri(c_int(18), (c_int * NUM)(1, 2, 3, 4, 5), c_int(NUM))
b = Ahri(c_int(12), (c_int * NUM)(5, 4, 3, 2, 1), c_int(NUM))
c = Ahri(c_int(15), (c_int * NUM)(*np.zeros(NUM, dtype=int)), c_int(NUM))
ahris = (Ahri * 3)(a, b, c)

ctypes_example.print_Ahri(ahris, 3)
ctypes_example.update_Ahri(ahris, 3)

for ahri in ahris:
    print(np.ctypeslib.as_array(ahri.score, shape=(NUM,)))

# C 全局变量直接赋值不可更改，需要调用函数
# AhriC.SOKYOEI = 100
ctypes_example.set_SOKYOEI(100)
ctypes_example.print_SOKYOEI()

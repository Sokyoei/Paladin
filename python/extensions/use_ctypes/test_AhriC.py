from ctypes import POINTER, Structure, c_char_p, c_int
from pathlib import Path
from typing import ClassVar, List, Tuple

import numpy as np

AhriC = np.ctypeslib.load_library("AhriC", Path(".").absolute())

# 2d array
arg = np.arange(9, dtype=c_int)
c_int_3x3_p = np.ctypeslib.ndpointer(dtype=c_int, ndim=2, shape=(3, 3))
# AhriC.array_add.argtypes = [c_int_3x3_p]
AhriC.array_add.restype = c_int_3x3_p
aa = np.ctypeslib.as_ctypes(arg)
ret = AhriC.array_add(aa)
print(np.ctypeslib.as_array(ret, shape=(3, 3)))


# struct
class Student(Structure):
    _fields_: ClassVar[List[Tuple]] = [("age", c_int), ("name", c_char_p)]


stus = (Student * 3)((1, "Ahri".encode()), (2, "Sokyoei".encode()), (3, "Nono".encode()))
# AhriC.student_add.argtypes = [POINTER(Student)]
AhriC.student_add.restype = POINTER(Student)
stus_ret = AhriC.student_add(stus)
for i in range(3):  # for i in stus_ret 会越界
    print(stus_ret[i].age, stus_ret[i].name)

from libcpp cimport *
from libcpp.string cimport *

def hello_cythoncpp():
    print("Hello Cython C++!")


cpdef add_cpythoncpp(int a, int b):
    cdef int c
    c = a + b
    return c


cdef class Human:
    cdef:
        string name
        int age

    def __cinit__(self, str name, int age):
        self.name = name.encode('utf-8')
        self.age = age

    def __dealloc__(self):
        pass

    property name:
        def __get__(self):
            return self.name.c_str().decode('utf-8')

    property age:
        def __get__(self):
            return self.age

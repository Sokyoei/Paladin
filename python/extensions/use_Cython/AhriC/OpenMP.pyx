from cython.parallel cimport parallel, prange
cimport openmp as omp

def f():
    cdef int i

    with nogil, parallel():
        for i in prange(10):
            i *= i

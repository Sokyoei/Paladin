from libc.stdio cimport *

ctypedef public struct Person:
    int age
    char * name

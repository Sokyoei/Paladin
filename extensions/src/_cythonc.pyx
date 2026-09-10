from libc.stdio cimport *
from libc.stdlib cimport *
from libc.stdint cimport *
from libc.string cimport *

def hello_cythonc():
    printf("Hello Cython C!\n")


ctypedef struct Animal:
    char* name
    int age


cdef Animal* _create_animal(const char* name, int age):
    cdef Animal* animal = <Animal*>malloc(sizeof(Animal))
    if animal == NULL:
        return NULL

    animal.name = <char*>malloc(strlen(name) + 1)
    if animal.name == NULL:
        free(animal)
        return NULL

    strcpy(animal.name, name)
    animal.age = age
    return animal


cdef void _destroy_animal(Animal* animal):
    if animal != NULL:
        free(animal.name)
        free(animal)


def create_animal(name: str, age: int):
    cdef bytes bname = name.encode('utf-8')
    cdef Animal* animal = _create_animal(bname, age)
    if animal == NULL:
        raise MemoryError("malloc Animal struct failed.")
    return <uintptr_t>animal


def destroy_animal(handle: int):
    if handle == 0:
        return
    cdef uintptr_t uptr = handle
    cdef Animal* animal = <Animal*>uptr
    _destroy_animal(animal)


def animal_get_name(handle: int):
    if handle == 0:
        raise ValueError("handle is null.")
    cdef uintptr_t uptr = handle
    cdef Animal* animal = <Animal*>uptr
    return animal.name.decode('utf-8')


def animal_get_age(handle: int):
    if handle == 0:
        raise ValueError("handle is null.")
    cdef uintptr_t uptr = handle
    cdef Animal* animal = <Animal*>uptr
    return animal.age

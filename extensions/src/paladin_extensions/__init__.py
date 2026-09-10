# pyright: reportMissingImports=false

import platform

from loguru import logger

if platform.system() == "Windows":
    import ctypes
    import os
    import sys

    buf = ctypes.create_unicode_buffer(512)
    ctypes.windll.kernel32.GetModuleFileNameW(ctypes.c_void_p(sys.dllhandle), buf, 512)
    py_dll_dir = os.path.dirname(buf.value)
    if os.path.isdir(py_dll_dir):
        os.add_dll_directory(py_dll_dir)


__all__ = []

try:
    from ._cpythonapi import add, dear, hello_cpython

    _cpythonapi = True
    __all__ += ["add", "dear", "hello_cpython"]
except ImportError as e:
    logger.warning(f"_cpythonapi import failed: {e}")
    _cpythonapi = False

try:
    from ._pybind11 import Person, add_ndarray_pybind11, add_pybind11, hello_pybind11

    _pybind11 = True
    __all__ += ["Person", "add_ndarray_pybind11", "add_pybind11", "hello_pybind11"]
except ImportError as e:
    logger.warning(f"_pybind11 import failed: {e}")
    _pybind11 = False

try:
    from ._cythonc import animal_get_age, animal_get_name, create_animal, destroy_animal, hello_cythonc

    _cythonc = True
    __all__ += ["animal_get_age", "animal_get_name", "create_animal", "destroy_animal", "hello_cythonc"]
except ImportError as e:
    logger.warning(f"_cythonc import failed: {e}")
    _cythonc = False

try:
    from ._cythoncpp import Human, add_cpythoncpp, hello_cythoncpp

    _cythoncpp = True
    __all__ += ["Human", "add_cpythoncpp", "hello_cythoncpp"]
except ImportError as e:
    logger.warning(f"_cythoncpp import failed: {e}")
    _cythoncpp = False

try:
    from ._fortran77 import hello_fortran77

    _fortran77 = True
    __all__ += ["hello_fortran77"]
except ImportError as e:
    logger.warning(f"_fortran77 import failed: {e}")
    _fortran77 = False

try:
    from ._fortran90 import ahri

    hello_fortran90 = ahri.hello_fortran90
    _fortran90 = True
    __all__ += ["hello_fortran90"]
except ImportError as e:
    logger.warning(f"_fortran90 import failed: {e}")
    _fortran90 = False

try:
    from ._rust import hello_rust

    _rust = True
    __all__ += ["hello_rust"]
except ImportError as e:
    logger.warning(f"_rust import failed: {e}")
    _rust = False

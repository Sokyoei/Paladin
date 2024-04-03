import sys

import numpy as np

if sys.version_info >= (3, 12) and np.__version__ >= "1.23.0":
    raise DeprecationWarning("numpy.distutils has been deprecated")

from numpy.distutils.core import Extension, setup

setup(
    name="f2py_example",
    author="Sokyoei",
    version="0.0.1",
    ext_modules=[
        Extension("f2py_example", sources=["src/f2py_example.f90"]),
        Extension("f2py_example_f77", sources=["src/f2py_example_f77.f"]),
    ],
)

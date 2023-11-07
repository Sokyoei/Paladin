import sys

import numpy as np

if sys.version_info >= (3, 12) and np.__version__ >= "1.23.0":
    raise DeprecationWarning("numpy.distutils has been deprecated")

from numpy.distutils.core import Extension, setup

setup(
    name="AhriF90",
    author="Sokyoei",
    version="0.0.1",
    ext_modules=[
        Extension("AhriF90", sources=["AhriF90.f90"]),
        Extension("AhriF77", sources=["AhriF77.f"]),
    ],
)

import numpy as np
from packaging import version
from setuptools import Extension, setup

if version.parse(np.__version__) < version.parse('2.0.0'):
    from numpy.distutils.core import Extension, setup  # pyright: ignore[reportMissingImports]

else:
    raise RuntimeError(f"numpy version: {np.__version__}, numpy.distutils is removed.")


setup(
    name="Paladin_extensions",
    author="Sokyoei",
    version="1.0.0",
    ext_modules=[
        Extension("_fortran77", sources=["src/_fortran77.F"]),
        Extension("_fortran90", sources=["src/_fortran90.f90"]),
    ],
)

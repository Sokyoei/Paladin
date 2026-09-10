from Cython.Build import cythonize
from pybind11.setup_helpers import Pybind11Extension
from setuptools import Extension, setup

ext_modules = cythonize(
    [
        Extension(name="_cythonc", sources=["src/_cythonc.pyx"]),
        Extension(name="_cythoncpp", sources=["src/_cythoncpp.pyx"], language="c++"),
    ]
)
ext_modules += [
    Pybind11Extension("_pybind11", sources=["src/_pybind11.cpp"]),
    # Extension("_pybind11", sources=["src/_pybind11.cpp"], include_dirs=[pybind11.get_include()]),
    Extension("_cpythonapi", sources=["src/_cpythonapi.c"]),
]

setup(name="Paladin_extensions", author="Sokyoei", version="1.0.0", ext_modules=ext_modules)

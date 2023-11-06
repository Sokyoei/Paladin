from pybind11 import get_include
from setuptools import Extension, setup

setup(name="use_pybind11", ext_modules=[Extension("AhriCXX", sources=["AhriCXX.cpp"], include_dirs=get_include())])

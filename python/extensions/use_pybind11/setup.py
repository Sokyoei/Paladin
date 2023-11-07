from pybind11 import get_include
from pybind11.setup_helpers import Pybind11Extension
from setuptools import Extension, setup

setup(
    name="use_pybind11",
    author="Sokyoei",
    version="0.0.1",
    ext_modules=[Pybind11Extension("AhriCXX", sources=["AhriCXX.cpp"])],
    # or
    # ext_modules=[Extension("AhriCXX", sources=["AhriCXX.cpp"], include_dirs=[get_include()])],
)

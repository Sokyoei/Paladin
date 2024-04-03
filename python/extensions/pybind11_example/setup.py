from pybind11 import get_include
from pybind11.setup_helpers import Pybind11Extension
from setuptools import Extension, setup

setup(
    name="pybind11_example",
    author="Sokyoei",
    version="0.0.1",
    ext_modules=[Pybind11Extension("pybind11_example", sources=["src/pybind11_example.cpp"])],
    # or
    # ext_modules=[Extension("pybind11_example", sources=["src/pybind11_example.cppp"], include_dirs=[get_include()])],
)

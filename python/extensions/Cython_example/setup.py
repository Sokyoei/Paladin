from Cython.Build import cythonize
from setuptools import Extension, setup

# python setup.py build_ext --inplace
setup(
    name="Cython_example",
    author="Sokyoei",
    version="0.0.1",
    ext_modules=cythonize(
        [
            Extension(name="c_example", sources=["src/c_example.pyx"]),
            Extension(name="cxx_example", sources=["src/cxx_example.pyx"], language="c++"),
        ]
    ),
)

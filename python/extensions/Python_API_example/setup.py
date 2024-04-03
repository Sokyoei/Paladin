from setuptools import Extension, setup

setup(name="Python_API_example", ext_modules=[Extension("Python_API_example", sources=["src/Python_API_example.c"])])

from setuptools import Extension, setup

setup(name="use_CPython_API", ext_modules=[Extension("AhriC", sources=["AhriC.c"])])

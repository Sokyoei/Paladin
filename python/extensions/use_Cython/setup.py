from Cython.Build import cythonize
from setuptools import Extension, setup


def get_module_list():
    pass


# python setup.py build_ext --inplace
setup(
    name="use_Cython",
    author="Sokyoei",
    version="0.0.1",
    ext_modules=cythonize(
        [
            Extension(name="AhriC.AhriC", sources=["AhriC/AhriC.pyx"], include_dirs=["AhriC"]),
            Extension(
                name="AhriC.OpenMP",
                sources=["AhriC/OpenMP.pyx"],
                include_dirs=["AhriC"],
                # MSVC
                extra_compile_args=["/openmp"],
                extra_link_args=["/openmp"],
                # GNU
                # extra_compile_args=["-openmp"],
                # extra_link_args=["-openmp"],
            ),
            Extension(
                name="AhriCXX.AhriCXX", sources=["AhriCXX/AhriCXX.pyx"], include_dirs=["AhriCXX"], language="c++"
            ),
        ]
    ),
)

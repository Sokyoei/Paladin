pkg_name = 'paladin_extensions'

_cpythonapi = py.extension_module(
    '_cpythonapi',
    sources: ['_cpythonapi.c'],
    dependencies: [py_dep, numpy_dep],
    # limited_api: '3.7',
    install: true,
    subdir: pkg_name,
)

_pybind11 = py.extension_module(
    '_pybind11',
    sources: ['_pybind11.cpp'],
    dependencies: [py_dep, numpy_dep, pybind11_dep],
    link_args: link_args,
    # pybind11 对 limited_api 支持有限
    # limited_api: '3.7',
    install: true,
    subdir: pkg_name,
)

_cythonc = py.extension_module(
    '_cythonc',
    sources: ['_cythonc.pyx'],
    dependencies: [py_dep, numpy_dep],
    install: true,
    subdir: pkg_name,
)

_cythoncpp = py.extension_module(
    '_cythoncpp',
    sources: ['_cythoncpp.pyx'],
    dependencies: [py_dep, numpy_dep],
    override_options: ['cython_language=cpp'],
    install: true,
    subdir: pkg_name,
)

_fortran77_c_source = custom_target(
    '_fortran77module.c',
    input: ['_fortran77.F'],
    output: ['_fortran77module.c', '_fortran77-f2pywrappers.f'],
    command: [
        py,
        '-m', 'numpy.f2py',
        '@INPUT@',
        '-m', '_fortran77',
        '--lower',
        '--build-dir', meson.current_build_dir(),
    ],
)

_fortran77 = py.extension_module(
    '_fortran77',
    sources: ['_fortran77.F', _fortran77_c_source, incdir_f2py / 'fortranobject.c'],
    dependencies: [py_dep, numpy_dep, f2py_dep],
    install: true,
    subdir: pkg_name,
)

_fortran90_c_source = custom_target(
    '_fortran90module.c',
    input: ['_fortran90.f90'],
    output: ['_fortran90module.c', '_fortran90-f2pywrappers2.f90'],
    command: [
        py,
        '-m', 'numpy.f2py',
        '@INPUT@',
        '-m', '_fortran90',
        '--lower',
        # NOTE: 需要加上，否则会在构建根路径下生成文件
        '--build-dir', meson.current_build_dir(),
    ],
)

_fortran90 = py.extension_module(
    '_fortran90',
    sources: ['_fortran90.f90', _fortran90_c_source, incdir_f2py / 'fortranobject.c'],
    dependencies: [py_dep, numpy_dep, f2py_dep],
    install: true,
    subdir: pkg_name,
)

py.install_sources(
    'paladin_extensions/__init__.py',
    subdir: pkg_name,
)

project(
    'paladin_extensions',
    'c',
    'cpp',
    'cython',
    'fortran',
    license: 'MIT',
    meson_version: '>=1.12.0',
    default_options: [
        'c_std=c99',
        'cpp_std=c++17',
        'buildtype=debugoptimized',
    ],
    version: '1.0.0',
)

cc = meson.get_compiler('c')
cxx = meson.get_compiler('cpp')

link_args = []
if cc.get_id() == 'gcc' and cxx.get_id() == 'gcc'
    # NOTE: Windows 下，仍然需要把动态库放在 pyd 的同级目录下，比如：libwinpthread-1.dll, libstdc++-6.dll,
    # libgcc_s_seh-1.dll, libgfortran-5.dll, libquadmath-0.dll, etc...
    link_args += ['-static-libgcc', '-static-libstdc++']
endif

fs = import('fs')
py = import('python').find_installation(pure: false)

py_dep = py.dependency()
numpy_dep = dependency('numpy')
incdir_f2py = run_command(
    py,
    ['-c', 'import numpy.f2py; print(numpy.f2py.get_include())'],
    check: true,
).stdout().strip()
f2py_dep = declare_dependency(include_directories: incdir_f2py)
pybind11_dep = dependency('pybind11')

cython = find_program('cython')
if not cython.found()
    error('Cython not found')
endif

subdir('src')

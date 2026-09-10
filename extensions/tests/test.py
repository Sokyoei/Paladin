# pyright: reportMissingImports=false

import numpy as np
import pytest


def test_cpythonapi():
    from paladin_extensions import add, dear, hello_cpython

    hello_cpython()

    assert dear() == "Dear Ahri Nono😍😘"
    assert add(1, 2) == 3
    assert add(1.1, 2.2) == pytest.approx(3.3)
    assert add(1, 2.2) == 3.2


def test_pybind11():
    from paladin_extensions import Person, add_ndarray_pybind11, add_pybind11, hello_pybind11

    hello_pybind11()
    nono = Person("Nono", 13)
    nono.print_info()

    assert add_pybind11(1, 2) == 3
    assert add_pybind11(1.1, 2.2) == pytest.approx(3.3)
    assert add_pybind11(1, 2.2) == 3.2

    a_arr = np.array([[1, 2], [3, 4]])
    b_arr = np.array([[5, 6], [7, 8]])
    c_arr = np.array([[6, 8], [10, 12]])
    assert (add_ndarray_pybind11(a_arr, b_arr) == c_arr).all()


def test_cythonc():
    from paladin_extensions import animal_get_age, animal_get_name, create_animal, destroy_animal, hello_cythonc

    hello_cythonc()

    animal = create_animal("Nono", 13)
    assert animal_get_name(animal) == "Nono"
    assert animal_get_age(animal) == 13
    destroy_animal(animal)


def test_cythoncpp():
    from paladin_extensions import Human, add_cpythoncpp, hello_cythoncpp

    hello_cythoncpp()

    assert add_cpythoncpp(1, 2) == 3

    human = Human("Nono", 13)
    assert human.name == "Nono"
    assert human.age == 13


def test_fortran77():
    from paladin_extensions import hello_fortran77

    hello_fortran77()


def test_fortran90():
    from paladin_extensions import hello_fortran90

    hello_fortran90()


def test_rust():
    from paladin_extensions import hello_rust

    hello_rust()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
python bytecode
"""

import dis
from typing import Literal


def f_string(n: int):
    return f"{n}"


def str_string(n: int):
    return str(n)


def if_elif_else(n: int) -> Literal[1, 2, 3, 4, 5, 0]:
    if n == 1:
        return 1
    elif n == 2:
        return 2
    elif n == 3:
        return 3
    elif n == 4:
        return 4
    elif n == 5:
        return 5
    else:
        return 0


def dict_get(n: int):
    return {
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
    }.get(n)


def add(a: int, b: int) -> int:
    a = a + 1
    return a + b


def radd(a: int, b: int) -> int:
    a += 1
    return a + b


if __name__ == "__main__":
    print(f"{'f_string':-^80}")
    dis.dis(f_string)
    print(f"{'str_string':-^80}")
    dis.dis(str_string)
    print(f"{'if_elif_else':-^80}")
    dis.dis(if_elif_else)
    print(f"{'dict_get':-^80}")
    dis.dis(dict_get)
    print(f"{'add':-^80}")
    dis.dis(add)
    print(f"{'radd':-^80}")
    dis.dis(radd)

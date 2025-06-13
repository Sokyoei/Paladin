"""
yield from
"""

from typing import Iterable


def flatten(items, ignore_types=(str, bytes)):
    for i in items:
        if isinstance(i, Iterable) and not isinstance(i, ignore_types):
            yield from flatten(i)
        else:
            yield i


def yield_():
    ahri = "ahri"
    sokyoei = "sokyoei"
    nono = "nono"
    for i in range(3):
        print("-")
        yield ahri
        print("--")
        yield sokyoei
        print("---")
        yield nono
        print("----")


if __name__ == '__main__':
    items = [1, 2, [3, 4, [5, [6], 7], 8, 9]]
    res = [i for i in flatten(items)]
    print(res)

    y = yield_()
    for i in y:
        print(i)
        print(12345)

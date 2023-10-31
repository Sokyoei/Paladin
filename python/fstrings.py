# f-string
# https://peps.python.org/pep-0498/
# https://docs.python.org/zh-cn/3/library/string.html#formatstrings

import sys

name = "Ahri"


class Person(object):

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return "__str__: self.name=%s, self.age=%d" % (self.name, self.age)

    def __repr__(self) -> str:
        return "__repr__: self.name=%s, self.age=%d" % (self.name, self.age)


p = Person("Sokyoei", 13)

print(p)
if sys.version_info >= (3, 8):
    print(f"{p!s}")
    print(f"{p!r}")

print("%s" % name)
if sys.version_info >= (2, 6):
    print("{0}".format(name))
if sys.version_info >= (3, 1):
    print("{}".format(name))
if sys.version_info >= (3, 6):
    print(f"name= {name}")
if sys.version_info >= (3, 8):
    print(f"{name=}")

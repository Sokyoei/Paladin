"""
generic 泛型
"""
import sys

if sys.version_info >= (3, 12):

    def add[T](a: T, b: T):
        return a + b

    print(add(1, 2))

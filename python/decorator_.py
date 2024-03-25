"""
decorator 装饰器

    在不改变原函数的情况下，对已有函数进行额外的功能扩展
    1. 不修改已有函数的源代码
    2. 不修改已有函数的调用方式
    3. 给已有函数增加额外的功能
"""

from functools import wraps


########################################################################################################################
# function decorator
########################################################################################################################
def time_logger(flag):  # 再包一层用来传递参数
    """
    Examples:
    >>> @time_logger(True)
    ... def foo(a, b):
    ...     print(a + b)

    >>> def doo(a, b):
    ...     print(a - b)

    >>> foo(1, 2)
    3
    hello world
    do something

    >>> # 输出 foo, 而不是 wrapper
    >>> print(foo.__name__)
    foo

    >>> print(doo.__name__)
    doo
    """

    def showtime(func):  # 装饰器的参数类型是函数，否则是闭包
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            print("hello world")
            if flag:
                print("do something")

        return wrapper

    return showtime


########################################################################################################################
# class decorator
########################################################################################################################
class Hello(object):
    """不带参数的类装饰器

    Examples:
    >>> @Hello
    ... def world(s):
    ...     print(s + "world")

    >>> world("llo ")
    hello world
    """

    def __init__(self, func):
        """接收被装饰函数"""
        self.__func = func

    def __call__(self, *args, **kwargs):
        """让对象变成可调用的对象"""
        print("he", end="")
        self.__func(*args, **kwargs)


class logger(object):
    """带参数的类装饰器

    Examples:
    >>> @logger(level="WARNING")
    ... def say(something):
    ...     print(f"say {something}!")

    >>> say("hello")  # doctest: +ELLIPSIS
    [WARNING]...
    say hello!...
    """

    def __init__(self, level="INFO"):
        """不再接收被装饰函数，而是接收传入参数"""
        self.level = level

    def __call__(self, func):
        """接收被装饰函数，实现装饰逻辑"""

        def wrapper(*args, **kwargs):
            print(f"[{self.level}]: the function {func.__name__}() is running...")
            func(*args, **kwargs)

        return wrapper


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

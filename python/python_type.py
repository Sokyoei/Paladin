# type 元类

from functools import partial
from inspect import getfullargspec as spec

endl = "\n"


class _Cout(object):
    def __init__(self): ...

    def __lshift__(self, *args):
        print(*args, end=" ")
        return self


Cout = _Cout()
Cout << "hello world" << endl

cout = type(
    '_',
    (),
    {
        "__lshift__": lambda self, *args: [print(*args, end=" "), self][
            -1
        ]  # [-1] TypeError: unsupported operand type(s) for <<: 'list' and 'str'
    },
)()  # () 实例化

cout << "hello world" << endl

F = type('_', (partial,), {'__ror__': lambda self, args: self(*args) if isinstance(args, tuple) else self(args)})
print(F(sum)([1, 2, 3]))

print(range(10) | F(filter, lambda x: x % 2) | F(sum))
print(F(sum).__ror__(F(filter, lambda x: x % 2).__ror__(range(10))))


class curry(object):
    def __init__(self, func):
        self.function = func
        self.args_len = len(spec(func).args)
        self.args_now = []

    def __or__(self, *args):
        self.args_now += args
        if len(self.args_now) < self.args_len:
            ret = self
        else:
            ret = self.function(*self.args_now)
            self.args_now.clear()
        return ret

    def __repr__(self):
        return self.args_now.__repr__()


@curry
def mean(a, b, c, d):
    print(sum([a, b, c, d]) / 4)


mean | 10 | 11 | 12 | 13  # 11.5

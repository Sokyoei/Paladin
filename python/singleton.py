"""
Singleton
"""

import threading


class AbstractSingleton(object):

    _instances = {}
    _locks = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._locks:
            cls._locks[cls] = threading.Lock()

        with cls._locks[cls]:
            if cls not in cls._instances:
                cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True


class TestSingleton(AbstractSingleton):

    def __init__(self, name):
        super().__init__()
        if not hasattr(self, 'name'):
            self.name = name

    def say_hello(self):
        print(f"Hello, I am {self.name}, id: {id(self)}")

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}, {id(self)})"


class TestSingleton2(AbstractSingleton):

    def __init__(self, name):
        super().__init__()
        if not hasattr(self, 'name'):
            self.name = name

    def say_hello(self):
        print(f"Hello, I am {self.name}, id: {id(self)}")

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}, {id(self)})"


def main():
    a = TestSingleton("Alice")
    b = TestSingleton("Bob")
    print(a)
    print(b)
    a.say_hello()
    b.say_hello()

    c = TestSingleton2("Alice")
    d = TestSingleton2("Bob")
    print(c)
    print(d)
    c.say_hello()
    d.say_hello()


if __name__ == '__main__':
    main()

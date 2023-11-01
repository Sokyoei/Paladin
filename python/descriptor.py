"""
descriptor 描述符
将一个类属性托管给一个类，这个属性就是一个描述符
非数据描述符 __get__()
数据描述符 __get__(), __set__() or(and) __delete__()
__getattribute__() > data descriptor > __init__() > non-data descriptor > __getattr__()
"""


class DataDescriptor(object):
    """数据描述符 (data descriptor)
    与被描述的类的 __init__() 参数重名时，优先调用数据描述符"""

    def __init__(self, default):
        self.prop = default
        print("DataDescriptor.__init__()")

    def __set__(self, instance, value):
        instance.__dict__[self.prop] = value
        print("DataDescriptor.__set__()")

    def __get__(self, instance, owner):
        print("DataDescriptor.__get__()")
        return instance.__dict__[self.prop]

    def __delete__(self, instance):
        del instance.__dict__[self.prop]
        print("DataDescriptor.__delete__()")


class NonDataDescriptor(object):
    """非数据描述符 (non-data descriptor),
    没有作为被描述的类的 __init__() 参数时，调用非数据描述符
    使数据不可更改"""

    def __init__(self, default=13):
        self._score = default
        print("NonDataDescriptor.__init__()")

    def __get__(self, instance, owner):
        print("NonDataDescriptor.__get__()")
        return self._score


class Student(object):
    school = "麻省理工学院"
    # 描述符必须在类中初始化，是类属性，不能在 __init__() 中初始化
    math = DataDescriptor("math")  # 数据描述符
    chinese = NonDataDescriptor()  # 非数据描述符

    def __init__(self, name=None, math=0, chinese=0):
        self.name = name
        self.math = math  # 不会覆盖数据描述符
        self.chinese = chinese  # 覆盖数据描述符
        print("Student.__init__()")

    def __getattribute__(self, item):
        """重载后，在调用所有的属性方法时，都会先调用 __getattribute__()"""
        print("Student.__getattribute__()")
        return super(Student, self).__getattribute__(item)

    def __getattr__(self, item):
        """重载后，在调用没有的属性方法时，才调用 __getattr()"""
        print("Student.__getattr__()")
        return 1111

    def __repr__(self):
        print("Student.__repr__()")
        return f"Student: {self.name}, math: {self.math}, chinese: {self.chinese}"

    def __str__(self):
        print("Student.__str__()")
        return f"Student: {self.name}, math: {self.math}, chinese: {self.chinese}"

    @staticmethod
    def do():
        print("do something")

    @classmethod
    def todo(cls):
        print("todo something")


if __name__ == "__main__":
    print(Student.__dict__)

    ahri = Student()
    ahri.math = 100
    # ahri.chinese = 20
    print(ahri)

    sokyoei = Student("Sokyoei", 156, 21)
    sokyoei.chinese = 21
    print(sokyoei)

# context manager 上下文管理器
# __enter__()
# __exit__()

import contextlib


class Resource(object):

    def __enter__(self):
        print("Resource.__enter__()")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Resource.__exit__()")
        return True

    @staticmethod
    def do():
        ahri  # noqa
        # 错误操作不会报错，因为 __exit__ return True
        print("do something")


with Resource() as r:
    r.do()


@contextlib.contextmanager  # [__enter__  yield  __exit__]
def resource(num):
    # __enter__
    print(f"{num}'s __enter__()")

    try:
        yield num
    # __exit__
    except Exception as e:
        print(e)
    finally:
        print(f"{num}'s __exit__()")
        return  # return 无返回值，从函数的任意深度跳出


with resource(1) as res1, resource(2) as res2:
    print(res1)
    print(res2)

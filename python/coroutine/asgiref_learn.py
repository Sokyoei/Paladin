"""
asgiref.sync async_to_sync/sync_to_async 同步异步相互无限嵌套调用
"""

from asgiref.sync import async_to_sync, sync_to_async


def sync1():
    print("1. sync 1")
    return async_to_sync(async1)(1, 2)


async def async1(a: int, b: int):
    print(f"2. async 1\ta + b = {a + b}")
    return await sync_to_async(sync2)(2, 3)


def sync2(x: int, y: int):
    print(f"3. sync 2\tx * y = {x * y}")
    return async_to_sync(async2)()


async def async2():
    print("4. async 2")
    return "async2"


def main():
    result = sync1()
    print(f"final result: {result}")


if __name__ == "__main__":
    main()

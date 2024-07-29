"""
Python 异步迭代器、异步生成器
@see https://peps.python.org/pep-0525/
"""

import asyncio
import sys
from typing import AsyncGenerator


async def generate_numbers(n: int) -> AsyncGenerator:
    for i in range(n):
        yield i
        await asyncio.sleep(1)


async def async_main():
    # 隐式调用
    print([i async for i in generate_numbers(10)])
    # python3.10 aiter() 显式调用
    if sys.version_info >= (3, 10):
        print([i async for i in aiter(generate_numbers(10))])


def main():
    pass


if __name__ == "__main__":
    asyncio.run(async_main())
    main()

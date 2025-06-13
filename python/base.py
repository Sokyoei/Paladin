import asyncio
from typing import Any, AsyncGenerator, Coroutine, Generator, Literal

int_: int = 1
float_: float = 1.1
str_: str = "1"
list_: list[int] = [1, 2, 3]
tuple_: tuple[int, int, int] = (1, 2, 3)
dict_: dict[int, str] = {1: "1", 2: "2"}


def function() -> Literal[1]:
    return 1


def generator() -> Generator[Literal[1], Any, None]:
    yield 1


async def coroutine() -> Coroutine:
    await asyncio.sleep(1)
    return


# https://peps.python.org/pep-0525/
async def async_generator() -> AsyncGenerator:
    await asyncio.sleep(1)
    yield


print(type(function()))
print(type(generator()))
print(type(coroutine()))
print(type(async_generator()))

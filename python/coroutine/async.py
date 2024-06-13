"""
Python 3.5: async/await
"""

import asyncio
import sys

from Paladin.utils import async_timer

if sys.version_info >= (3, 5):

    @async_timer
    async def do_some_thing(x: int):
        print(f"waiting {x} second start")
        await asyncio.sleep(x)
        print(f"waiting {x} second end")

else:

    @async_timer
    @asyncio.coroutine
    def do_some_thing(x: int):
        print(f"waiting {x} second start")
        yield from asyncio.sleep(3)
        print(f"waiting {x} second end")


async def async_main():
    # 并发执行协程
    # 方式一
    task1 = asyncio.create_task(do_some_thing(1))
    task2 = asyncio.create_task(do_some_thing(2))
    print("create_task start")
    await task1
    await task2
    print("create_task end")
    # 方式二
    if sys.version_info >= (3, 11):
        async with asyncio.TaskGroup() as tg:
            tg.create_task(do_some_thing(1))
            tg.create_task(do_some_thing(2))
            print("TaskGroup start")
        print("TaskGroup end")
    # 方式三
    print("gather start")
    await asyncio.gather(do_some_thing(1), do_some_thing(2), do_some_thing(3))
    print("gather end")


def main():
    loop = asyncio.get_event_loop()
    # loop = asyncio.get_running_loop()
    if sys.version_info >= (3, 11):
        tasks = [
            loop.create_task(do_some_thing(1)),
            loop.create_task(do_some_thing(2)),
            loop.create_task(do_some_thing(3)),
        ]
    else:
        tasks = [do_some_thing(1), do_some_thing(2), do_some_thing(3)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == "__main__":
    asyncio.run(async_main())
    # asyncio 在主线程中仅生成一个事件循环
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    main()

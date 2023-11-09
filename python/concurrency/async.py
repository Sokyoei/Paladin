"""
Python 3.5: async/await
"""

import asyncio
import sys

if sys.version_info >= (3, 8):

    async def wash():
        await asyncio.sleep(3)
        print("wash finished")

else:

    @asyncio.coroutine
    def wash():
        yield from asyncio.sleep(3)
        print("wash finished")


async def wash2():
    await asyncio.sleep(5)
    print("wash2 finished")


async def wash3():
    await asyncio.sleep(2)
    print("wash3 finished")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if sys.version_info >= (3, 11):
        tasks = [loop.create_task(wash()), loop.create_task(wash2()), loop.create_task(wash3())]
    else:
        tasks = [wash(), wash2(), wash3()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

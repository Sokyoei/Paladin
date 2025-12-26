import redis
from redis import asyncio as aioredis
from starlette.applications import Starlette

from .config import REDIS_URI


class RedisManager(object):

    def __init__(self):
        pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
        self.r = redis.Redis(connection_pool=pool, charset="utf8", decode_responses=True)

    def start(self):
        pass

    def close(self):
        pass


class AsyncRedisManager(object):

    def __init__(self):
        self.r = aioredis.from_url(REDIS_URI)

    def init_app(self, app: Starlette):
        pass

    async def start(self):
        pass

    async def close(self):
        pass

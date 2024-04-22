import redis
from redis import asyncio as aioredis

REDIS_URL = "redis://localhost"


class RedisConfig(object):
    def __init__(self):
        pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
        self.r = redis.Redis(connection_pool=pool, charset="utf8", decode_responses=True)

    def start(self):
        pass

    def close(self):
        pass


class AsyncRedisConfig(object):
    def __init__(self):
        self.r = aioredis.from_url(REDIS_URL)

    async def start(self):
        pass

    async def close(self):
        pass

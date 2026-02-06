from redis import asyncio as aioredis

from Ahri.Paladin.config import settings


class AsyncRedisManager(object):

    def __init__(self):
        self._redis = None

    async def start(self):
        self._redis = await aioredis.from_url(settings.REDIS_URI)

    async def close(self):
        if self._redis:
            await self._redis.aclose()
            self._redis = None


aioredis_manager = AsyncRedisManager()

from fastapi import FastAPI
from loguru import logger
from redis import asyncio as aioredis

from .config import REDIS_URI


class AsyncRedisManager(object):

    def __init__(self):
        self.__redis: aioredis.Redis | None = None

    @property
    def redis(self) -> aioredis.Redis:
        if not self.__redis:
            raise ValueError("Redis connection not initialized")
        return self.__redis

    async def start(self, app: FastAPI):
        self.__redis = await aioredis.from_url(REDIS_URI)
        self.__redis.ping()
        logger.info("Redis connection successfully")
        app.state.redis = self.__redis

    async def close(self):
        if self.__redis:
            await self.__redis.aclose()
            self.__redis = None
            logger.info("Redis connection closed")


aioredis_manager = AsyncRedisManager()

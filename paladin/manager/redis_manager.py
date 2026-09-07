import redis

from paladin.config import settings


class RedisManager:

    def __init__(self):
        self._redis = None

    def start(self):
        self._redis = redis.from_url(settings.REDIS_URI)

    def close(self):
        self._redis.close()


redis_manager = RedisManager()

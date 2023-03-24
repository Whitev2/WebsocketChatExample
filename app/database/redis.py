from datetime import datetime

import redis.asyncio as aioredis
import json
from redis.asyncio.connection import ConnectionPool

from config import config


class RedRedis:
    main_base = 0
    data_redis: ConnectionPool

    @classmethod
    async def connect_to_storage(cls):

        cls.data_redis = await aioredis.from_url(
            f"{config.RedisUrl}{cls.main_base}", decode_responses=True)


class DataRedis(RedRedis):

    @classmethod
    async def set_key(cls, keys: str, data: str, ttl=-1):

        return await cls.data_redis.set(
            keys, data, ex=ttl
        )



    @classmethod
    async def get_data(cls, key: str):
        return await cls.data_redis.get(key)

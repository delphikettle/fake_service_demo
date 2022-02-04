from asyncio import get_event_loop
from typing import Union

from arq import ArqRedis
from arq.connections import RedisSettings, create_pool
from peewee import Proxy

arq_redis: Union[ArqRedis, Proxy] = Proxy()


def init_redis(settings: RedisSettings):
    pool = get_event_loop().run_until_complete(create_pool(settings))
    arq_redis.initialize(pool)

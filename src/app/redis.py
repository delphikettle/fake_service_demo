from dataclasses import dataclass
from typing import Union

from arq import ArqRedis
from arq.connections import RedisSettings, create_pool
from peewee import Proxy

from app.models.task import Task
from utils.config import ConfigBase


@dataclass
class RedisConfig(RedisSettings, ConfigBase):
    @classmethod
    def _set_current(cls, conf: 'RedisConfig'):
        redis_settings.initialize(conf)
        _arq_redis.initialize(None)


redis_settings: Union[RedisConfig, Proxy] = Proxy()
_arq_redis: Union[ArqRedis, Proxy] = Proxy()


async def enqueue_task(task: Task):
    if _arq_redis.obj is None:
        _arq_redis.initialize(await create_pool(redis_settings))

    await _arq_redis.enqueue_job('handle_task', task.id)

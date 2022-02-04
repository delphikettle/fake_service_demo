from dataclasses import dataclass, asdict, field
from typing import Optional, Union

from arq.connections import RedisSettings
from peewee import Proxy
from peewee_async import PooledPostgresqlDatabase

from app.models.base import apply_db
from app.redis import init_redis
from utils.config import ConfigBase


@dataclass
class DBConfig(ConfigBase):
    password: Optional[str] = None
    host: str = 'localhost'
    port: int = 5433
    database: str = 'fake_app'
    user: str = 'postgres'

    @classmethod
    def _set_current(cls, conf: 'ConfigBase'):
        d = asdict(conf)
        apply_db(PooledPostgresqlDatabase(**d))


@dataclass
class RedisConfig(RedisSettings, ConfigBase):
    @classmethod
    def _set_current(cls, conf: 'RedisConfig'):
        init_redis(conf)


@dataclass
class AppConfig(ConfigBase):
    db: DBConfig = field(default_factory=DBConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)

    @classmethod
    def _set_current(cls, conf: 'ConfigBase'):
        config.initialize(conf)


config: Union[AppConfig, Proxy] = Proxy()

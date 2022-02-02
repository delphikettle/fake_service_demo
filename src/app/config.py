from dataclasses import dataclass, asdict
from typing import Optional

from peewee import Proxy
from peewee_async import PooledPostgresqlDatabase

from app.models.base import apply_db
from utils.config import ConfigBase


@dataclass
class AppConfig(ConfigBase):
    password: Optional[str] = None
    host: str = 'localhost'
    port: int = 5433
    database: str = 'fake_app'
    user: str = 'postgres'

    @classmethod
    def _set_current(cls, conf: 'ConfigBase'):
        config.initialize(conf)
        d = asdict(conf)

        apply_db(PooledPostgresqlDatabase(**d))


config: AppConfig = Proxy()

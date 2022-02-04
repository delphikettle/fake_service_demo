from dataclasses import field, dataclass
from typing import Union

from peewee import Proxy

from api.config import ApiConfig
from app.config import AppConfig
from utils.config import ConfigBase
from worker.config import WorkerConfig


@dataclass
class FakeAppConfig(ConfigBase):
    app: AppConfig = field(default_factory=AppConfig)
    api: ApiConfig = field(default_factory=ApiConfig)
    worker: WorkerConfig = field(default_factory=WorkerConfig)

    @classmethod
    def _set_current(cls, conf: 'ConfigBase'):
        config.initialize(conf)


config: Union[FakeAppConfig, Proxy] = Proxy()

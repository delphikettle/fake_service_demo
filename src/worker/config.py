from dataclasses import dataclass
from typing import Union

from peewee import Proxy

from utils.config import ConfigBase


@dataclass
class WorkerConfig(ConfigBase):
    fail_time: int = 13

    @classmethod
    def _set_current(cls, conf: 'ConfigBase'):
        config.initialize(conf)


config: Union[WorkerConfig, Proxy] = Proxy()

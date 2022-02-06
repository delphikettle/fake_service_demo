from dataclasses import dataclass
from typing import Union

from peewee import Proxy

from utils.config import ConfigBase


@dataclass
class ApiConfig(ConfigBase):
    host: str = '0.0.0.0'
    port: int = 4321

    @classmethod
    def _set_current(cls, conf: 'ConfigBase'):
        config.initialize(conf)


config: Union[ApiConfig, Proxy] = Proxy()

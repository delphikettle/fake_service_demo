from dataclasses import dataclass, field

from app.config import AppConfig
from utils.config import ConfigBase


@dataclass
class MigrationsConfig(ConfigBase):
    app: AppConfig = field(default_factory=AppConfig)

    @classmethod
    def _set_current(cls, conf: 'ConfigBase'):
        pass

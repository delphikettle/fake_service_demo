from dataclasses import dataclass, field

from app.config import AppConfig
from utils.config import ConfigBase


@dataclass
class WorkerConfig(ConfigBase):
    app: AppConfig = field(default=AppConfig)

import logging
from abc import abstractmethod
from dataclasses import dataclass, fields

import dacite
import yaml

logger = logging.getLogger(__name__)


@dataclass
class ConfigBase:
    @classmethod
    def load_from_dict(cls, data: dict, as_current=True):
        conf = dacite.from_dict(cls, data)
        if as_current:
            cls.set_current(conf)
        return conf

    @classmethod
    def set_current(cls, conf: 'ConfigBase'):
        cls._set_current(conf)
        for field in fields(conf):
            v = getattr(conf, field.name)
            if isinstance(v, ConfigBase):
                type(v).set_current(v)

    @classmethod
    @abstractmethod
    def _set_current(cls, conf: 'ConfigBase'):
        pass

    @classmethod
    def load_from_file(cls, filename, as_current=True):
        logger.info(f'Loading config {cls} from {filename}')
        conf_data = yaml.safe_load(open(filename))
        cls.load_from_dict(conf_data, as_current=as_current)

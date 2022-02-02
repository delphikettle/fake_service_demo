from enum import Enum
from typing import Mapping, Iterable, Union, Any, Type

from peewee import IntegerField


class OptionsField(IntegerField):
    def __init__(
        self, options: Union[Iterable, Mapping[int, Any], Type[Enum]] = None, **kwargs
    ):
        super().__init__(**kwargs)
        if options is None:
            return
        if issubclass(options, Enum):
            options = {int(i.value): i for i in options}
        elif not isinstance(options, Mapping):
            options = dict(enumerate(options))

        assert all(isinstance(k, int) for k in options.keys())
        self._options = options

    @property
    def options(self):
        return self._options.values()

    def python_value(self, value):
        if value is None:
            return
        if isinstance(value, int):
            return self._options[value]
        if value not in self.options:
            raise ValueError(f"There's no such option: {value}")
        return value

    def adapt(self, value):
        if value is None:
            return
        if isinstance(value, Enum):
            value = value.value
        if value in self._options:
            return value
        for i, item in self._options.items():
            if item == value:
                return i
        raise ValueError(f"There's no such option: {value}")

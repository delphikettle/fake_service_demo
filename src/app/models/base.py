import logging
from typing import Union, Set, Type
from uuid import uuid4

from peewee import Proxy, PostgresqlDatabase, Model, UUIDField
from peewee_async import Manager, AsyncDatabase

db: Union[AsyncDatabase, PostgresqlDatabase, Proxy] = Proxy()
manager: Union[Manager, Proxy] = Proxy()

logger = logging.getLogger(__name__)


def apply_db(new_db: PostgresqlDatabase):
    logger.info(f'Connecting database to {new_db.connect_params}')
    db.initialize(new_db)
    manager.initialize(Manager(db.obj))

    new_db.bind(BaseModel.all_models(), bind_refs=False, bind_backrefs=False)

    db.connection()
    logger.info(f'Connected database to {new_db.connect_params}')


class BaseModel(Model):
    id = UUIDField(default=uuid4, primary_key=True)

    @classmethod
    def all_models(cls) -> Set[Type['BaseModel']]:
        models = set(cls.__subclasses__())
        for model in list(models):
            models = models | model.all_models()
        return models

    def dict(self) -> dict:
        return {field.name: getattr(self, field.name) for field in self._meta.sorted_fields}

    class Meta:
        database = db

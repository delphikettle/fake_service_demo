from os.path import abspath, dirname, join

from peewee import PostgresqlDatabase

from app.migrations.config import MigrationsConfig
from app.models.base import BaseModel, db
from utils.tests import TestCaseWithDB, TemplatedPostgresqlFactory


class BaseTestCase(TestCaseWithDB):
    factory = TemplatedPostgresqlFactory(
        BaseModel, abspath(join(dirname(__file__), '..', 'app', 'migrations'))
    )

    def get_peewee_db(self, dsn: dict) -> PostgresqlDatabase:
        MigrationsConfig.load_from_dict({'app': dsn})
        return db.obj

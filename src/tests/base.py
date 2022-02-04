from os.path import abspath, dirname, join
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from peewee import PostgresqlDatabase

from app.config import AppConfig
from app.models.base import BaseModel, db
from utils.tests import TestCaseWithDB, TemplatedPostgresqlFactory


class BaseTestCase(IsolatedAsyncioTestCase, TestCaseWithDB):
    factory = TemplatedPostgresqlFactory(
        BaseModel, abspath(join(dirname(__file__), '..', 'app', 'migrations'))
    )

    def get_peewee_db(self, dsn: dict) -> PostgresqlDatabase:
        self.apply_dsn(dsn)
        return db.obj

    def apply_dsn(self, dsn):
        with patch('app.redis.create_pool'):
            AppConfig.load_from_dict({'db': dsn})

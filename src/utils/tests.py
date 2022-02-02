import atexit
import logging
import secrets
import traceback
from abc import abstractmethod
from contextlib import closing
from threading import Lock
from unittest import TestCase

import peewee
import psycopg2
from peewee_migrate import Router
from psycopg2 import ProgrammingError


class TemplatedPostgresqlFactory:
    db: peewee.Proxy
    migrations_dir: str

    def __init__(
        self,
        base_model,
        migrations_dir: str,
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password=None,
    ):
        self.migrations_dir = migrations_dir
        self.base_model = base_model
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self._lock = Lock()
        self._id = f'{id(self) + secrets.randbits(8):x}'
        self._template_name = f'tests_{self._id}_template'
        self._created = False
        atexit.register(self.clear)

    def __call__(self, test_case: 'TestCaseWithDB') -> peewee.PostgresqlDatabase:
        self._create_template_db(test_case)
        db_name = self._create_db(False)
        return self.get_peewee_db(self.dsn(database=db_name), test_case)

    def _create_template_db(self, test_case: 'TestCaseWithDB'):
        with self._lock:
            if not self._created:
                self._create_db(True)
                db = self.init_db(self.dsn(database=self._template_name), test_case=test_case)
                db.close()
                self._created = True
        return self._template_name

    def _create_db(self, is_template=False):
        if is_template:
            db_name = self._template_name
            q_suf = 'is_template TRUE'
            logging.info(f'Creating template db {self._template_name}')
        else:
            id_ = f'{secrets.randbits(32):08x}'
            db_name = f'tests_{self._id}_{id_}'
            q_suf = f'template {self._template_name}'
            logging.info(f'Creating db {db_name} from template {self._template_name}')
        with closing(psycopg2.connect(**self.dsn(database='postgres'))) as conn:
            conn.autocommit = True
            with closing(conn.cursor()) as cursor:
                cursor.execute(f'CREATE DATABASE {db_name} ' + q_suf)
        return db_name

    def get_peewee_db(self, dsn: dict, test_case: 'TestCaseWithDB'):
        logging.debug('Connecting to db', dsn)
        peewee_db = test_case.get_peewee_db(dsn)
        return peewee_db

    def init_db(self, dsn: dict, test_case: 'TestCaseWithDB'):
        temp_db = self.get_peewee_db(dsn, test_case=test_case)
        Router(temp_db, self.migrations_dir).run()
        return temp_db

    @classmethod
    def all_models(cls, model):
        return set(model.__subclasses__()).union(
            [s for c in model.__subclasses__() for s in cls.all_models(c)]
        )

    def dsn(self, **kwargs):
        params = dict(kwargs)
        params.setdefault('port', self.port)
        params.setdefault('host', self.host)
        params.setdefault('user', self.user)
        params.setdefault('database', 'test')
        params.setdefault('password', self.password)

        return params

    def clear(self, db_name=None):
        with closing(psycopg2.connect(**self.dsn(database='postgres'))) as conn:
            conn.autocommit = True
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    f"SELECT datname, datistemplate FROM pg_database WHERE datname like 'tests_{self._id}%'"
                )
                if db_name is None:
                    dbs = cursor.fetchall()
                else:
                    dbs = [(db_name, False)]
                for db_name, is_template in dbs:
                    if is_template:
                        cursor.execute(f'ALTER DATABASE {db_name} is_template FALSE')
                    cursor.execute(
                        f'SELECT pg_terminate_backend(pg_stat_activity.pid) '
                        f'FROM pg_stat_activity '
                        f"WHERE pg_stat_activity.datname = '{db_name}';"
                    )
                    try:
                        cursor.execute(f'DROP DATABASE {db_name}')
                        logging.info(f'Cleared {db_name} database')
                    except ProgrammingError:
                        logging.warning('Failed to clear', db_name)
                        traceback.print_exc()

    def __del__(self):
        self.clear()


class TestCaseWithDB(TestCase):
    def setUp(self):
        super().setUp()
        self.db = self.factory(self)

    def tearDown(self):
        self.db.close()
        self.factory.clear(self.db.database)
        super().tearDown()

    @property
    @abstractmethod
    def factory(self) -> TemplatedPostgresqlFactory:
        pass

    @abstractmethod
    def get_peewee_db(self, dsn: dict) -> peewee.PostgresqlDatabase:
        pass

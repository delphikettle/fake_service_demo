from unittest.mock import patch

from httpx import AsyncClient

from api.app import create_app
from config import FakeAppConfig
from tests.base import BaseTestCase


class APIBaseTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.app = create_app()
        self.aclient = AsyncClient(app=self.app, base_url='http://test', follow_redirects=True)
        self._enqueue_mock = patch('api.task.enqueue_task')
        self.enqueue_mock = self._enqueue_mock.start()

    def tearDown(self):
        super().tearDown()
        self._enqueue_mock.stop()

    def apply_dsn(self, dsn):
        with patch('app.redis.create_pool'):
            FakeAppConfig.load_from_dict({'app': {'db': dsn}})

    def assert_dict_sourced(self, source_dict, check_dict):
        self.assertDictEqual(check_dict, {**check_dict, **source_dict})

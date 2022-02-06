import testing.redis
from httpx import AsyncClient

from api.app import create_app
from config import FakeAppConfig
from tests.base import BaseTestCase
from worker.worker import create_worker


class IntegrationBaseTestCase(BaseTestCase):
    async def burst_worker(self):
        self.worker = create_worker(burst=True)
        await self.worker.main()

    def setUp(self):
        self.redis_server = testing.redis.RedisServer()
        super().setUp()
        self.app = create_app()
        self.aclient = AsyncClient(app=self.app, base_url='http://test', follow_redirects=True)

    def tearDown(self):
        super().tearDown()
        self.redis_server.stop()

    def apply_dsn(self, dsn):
        FakeAppConfig.load_from_dict({'app': {'db': dsn, 'redis': self.redis_server.dsn()}})

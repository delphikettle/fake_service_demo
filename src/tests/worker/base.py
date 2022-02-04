import testing.redis

from config import FakeAppConfig
from tests.base import BaseTestCase
from worker.worker import create_worker


class WorkerBaseTestCase(BaseTestCase):
    async def burst_worker(self):
        self.worker = create_worker(burst=True)
        await self.worker.main()

    def setUp(self):
        self.redis_server = testing.redis.RedisServer()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.redis_server.stop()

    def apply_dsn(self, dsn):
        FakeAppConfig.load_from_dict({'app': {'db': dsn, 'redis': self.redis_server.dsn()}})

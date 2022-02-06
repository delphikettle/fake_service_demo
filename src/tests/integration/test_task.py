from unittest.mock import patch

from app.models.task import TaskStatus
from tests.integration.base import IntegrationBaseTestCase


class TaskIntegrationTestCase(IntegrationBaseTestCase):
    async def test_task_creation(self):
        proc_time = 10
        new_task = {'name': 'test_name', 'processing_time': proc_time}
        resp = await self.aclient.post('/tasks', json=new_task)

        resp = await self.aclient.get(f'/tasks/{resp.json()["task_id"]}')
        assert resp.json()['status'] == TaskStatus.NEW.value
        with patch('worker.tasks.sleep') as sleep_mock:
            await self.burst_worker()
            assert sleep_mock.call_count == 1
            assert sleep_mock.call_args_list[0].args[0] == proc_time

        resp = await self.aclient.get(f'/tasks/{resp.json()["task_id"]}')
        assert resp.json()['status'] == TaskStatus.COMPLETED.value

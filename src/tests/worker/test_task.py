from unittest.mock import patch

from app.models.base import manager
from app.models.task import Task, TaskStatus
from app.redis import enqueue_task
from tests.worker.base import WorkerBaseTestCase


class WorkerTaskTestCase(WorkerBaseTestCase):
    async def test_task_called(self):
        proc_time = 10
        task = await manager.create(Task, name='test', processing_time=proc_time)
        await enqueue_task(task)
        with patch('worker.tasks.sleep') as sleep_mock:
            await self.burst_worker()
            assert sleep_mock.call_count == 1
            assert sleep_mock.call_args_list[0].args[0] == proc_time

        task = await manager.get(Task, id=task.id)
        assert task.status == TaskStatus.COMPLETED

    async def test_task_failed(self):
        proc_time = 13
        task = await manager.create(Task, name='test', processing_time=proc_time)
        await enqueue_task(task)
        with patch('worker.tasks.sleep') as sleep_mock:
            await self.burst_worker()
            assert sleep_mock.call_count == 1
            assert sleep_mock.call_args_list[0].args[0] == proc_time

        task = await manager.get(Task, id=task.id)
        assert task.status == TaskStatus.ERROR

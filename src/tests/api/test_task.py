from asyncio import gather
from random import randint
from uuid import UUID

from tests.api.base import APIBaseTestCase


class APITaskTestCase(APIBaseTestCase):
    async def test_task_creation(self):
        new_task = {'name': 'test_name', 'processing_time': 10}
        resp = await self.aclient.post('/tasks', json=new_task)
        self.enqueue_mock.assert_called()
        assert self.enqueue_mock.call_args_list[0].args[0].id == UUID(resp.json()['task_id'])
        self.assert_dict_sourced(new_task, resp.json())

        resp = await self.aclient.get(f'/tasks/{resp.json()["task_id"]}')
        self.assert_dict_sourced(new_task, resp.json())

    async def test_tasks_list(self):
        new_tasks = {
            f'test_name_{i}': {'name': f'test_name_{i}', 'processing_time': randint(1, 15)}
            for i in range(10)
        }
        await gather(
            *(self.aclient.post('/tasks', json=new_task) for new_task in new_tasks.values())
        )
        resp = await self.aclient.get('/tasks')
        for task in resp.json():
            self.assert_dict_sourced(new_tasks.pop(task['name']), task)
        assert not new_tasks

from unittest import IsolatedAsyncioTestCase

import pytest

from app.models.base import manager
from app.models.task import Task, TaskStatus
from tests.base import BaseTestCase


@pytest.mark.asyncio
class BasicTestCase(IsolatedAsyncioTestCase, BaseTestCase):
    async def test_task(self):
        task0 = await manager.create(
            Task, name='test_name', processing_time=10, status=TaskStatus.ERROR
        )
        task1 = await manager.get(Task)
        assert task0 == task1

from asyncio import sleep
from logging import getLogger
from typing import Union
from uuid import UUID

from app.models.base import manager
from app.models.task import Task, TaskStatus
from worker import config

logger = getLogger(__name__)


async def _process_task(task: Task):
    if task.processing_time == config.fail_time:
        raise ValueError(f'Wrong processing time: {task.processing_time}')
    await sleep(task.processing_time)


async def handle_task(ctx, task_id: Union[str, UUID]):
    task = await manager.get(Task, id=task_id)
    task.status = TaskStatus.PROCESSING
    await manager.update(task)
    try:
        await _process_task(task)
        task.status = TaskStatus.COMPLETED
        await manager.update(task)
    except Exception as e:
        task.status = TaskStatus.ERROR
        await manager.update(task)
        logger.exception(e)
        raise

from typing import List
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

from app.models.base import manager
from app.models.task import Task, TaskStatus
from app.redis import arq_redis

tasks_router = APIRouter()


class NewTaskModel(BaseModel):
    name: str
    processing_time: int


class TaskModel(BaseModel):
    task_id: UUID
    name: str
    processing_time: int
    status: TaskStatus


@tasks_router.post('/', response_model=TaskModel)
async def create_task(new_task: NewTaskModel):
    task = await manager.create(
        Task, name=new_task.name, processing_time=new_task.processing_time
    )
    await arq_redis.enqueue_job('handle_task', task.id)
    return task.dict()


@tasks_router.get('/{id_}', response_model=TaskModel)
async def get_task(id_):
    return (await manager.get(Task, id=id_)).dict()


@tasks_router.get('/', response_model=List[TaskModel])
async def get_tasks():
    return [task.dict() for task in await manager.execute(Task.select())]

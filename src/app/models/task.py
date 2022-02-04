from enum import Enum

from peewee import TextField, IntegerField

from app.models.base import BaseModel
from utils.fields import OptionsField


class TaskStatus(Enum):
    NEW, PROCESSING, COMPLETED, ERROR = range(1, 5)


class Task(BaseModel):
    name = TextField(unique=True, null=False)
    processing_time = IntegerField(null=False)
    status = OptionsField(TaskStatus, null=False, default=TaskStatus.NEW)

    def dict(self) -> dict:
        res = super().dict()
        res['task_id'] = res.pop('id')
        return res

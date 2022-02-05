from arq import Worker

from app.redis import redis_settings
from worker.tasks import handle_task


def create_worker(**kwargs):
    return Worker(
        redis_settings=redis_settings, functions=(handle_task,), handle_signals=False, **kwargs
    )

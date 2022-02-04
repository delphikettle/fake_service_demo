from arq import Worker

from app.redis import arq_redis
from worker.tasks import handle_task


def create_worker(**kwargs):
    return Worker(
        functions=(handle_task,), redis_pool=arq_redis.obj, handle_signals=False, **kwargs
    )

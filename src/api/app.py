from fastapi import FastAPI
from uvicorn import Server
from uvicorn.config import Config

from api import config
from api.exceptions import add_exception_handlers
from api.task import tasks_router
from app.migrations.cli import check_migrations


def create_app():
    app = FastAPI()
    app.include_router(tasks_router, prefix='/tasks', tags=['tasks'])
    add_exception_handlers(app)
    return app


def run_server():
    app = create_app()
    check_migrations()
    uvicorn_config = Config(app=app, host=config.host, port=config.port,)
    Server(uvicorn_config).run()

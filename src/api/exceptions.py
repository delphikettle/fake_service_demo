import logging
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from peewee import DoesNotExist, IntegrityError
from starlette.responses import JSONResponse


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(DoesNotExist)
    async def not_found_error(req, exc: DoesNotExist):
        model_name = exc.__class__.__name__.replace('DoesNotExist', '')
        mes = f'{model_name} is not found' if model_name else 'Not found'
        if exc.args:
            mes += f': {";".join(exc.args)}'
        logging.exception(mes)
        return await http_exception_handler(req, HTTPException(404, mes))

    @app.exception_handler(IntegrityError)
    async def integrity_error(req, exc: IntegrityError):
        desc, detail, _ = exc.args[0].split('\n')
        detail = detail.replace('ERROR: ', '')
        logging.exception(detail)
        return JSONResponse({'description': desc, 'detail': detail}, status_code=409)

    @app.exception_handler(ValueError)
    async def value_error(req, exc: ValueError):

        logging.exception(exc)
        return await http_exception_handler(req, HTTPException(400, ';'.join(exc.args)))

    @app.exception_handler(Exception)
    async def generic_exception(req, exc: Exception):
        exc_info = traceback.format_exc()
        return JSONResponse(
            {
                'traceback': exc_info,
                'description': ';'.join(exc.args),
                'detail': exc.__class__.__name__,
            },
            status_code=500,
        )

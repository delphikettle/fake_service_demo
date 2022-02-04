import logging
import sys

import click

from api.app import run_server
from config import FakeAppConfig
from worker.worker import create_worker


@click.group()
@click.option('--conf', '-c', default='conf.yaml')
def cli(conf):
    FakeAppConfig.load_from_file(conf)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@cli.command('api')
def run_api():
    run_server()


@cli.command('worker')
def run_worker():
    create_worker().run()


if __name__ == '__main__':
    cli()

from os.path import dirname

import click
from peewee_migrate import Router

from app.migrations.config import MigrationsConfig
from app.models.base import db

router = Router(db, dirname(__file__))


@click.group()
@click.option('--conf', '-c', default='./src/conf.yaml')
def cli(conf):
    MigrationsConfig.load_from_file(conf)


@cli.command('create')
@click.argument('migration_name', required=False, default='migration')
def create_migration(migration_name='migration'):
    with db.allow_sync():
        router.create(migration_name, auto='app.models')
        click.echo('Migration created, please modify redundant stuff')


@cli.command('apply')
def apply_migrations():
    with db.allow_sync():
        router.run(fake=False)


@cli.command('check')
def check_migrations():
    with db.allow_sync():
        if router.diff:
            raise RuntimeError(
                f'Not all migrations are applied: {router.diff}'
                'Please apply them using `./src/app/migraions/cli.py` script'
            )


if __name__ == '__main__':
    cli()

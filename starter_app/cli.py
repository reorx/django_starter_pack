import click
import logging

from .utils.django_integration import setup_starter_app

setup_starter_app()

from .log import lg, set_logger
from .subapp.models import LogicUnit # noqa




@click.group()
@click.option('-d', '--debug', is_flag=True)
def cli(debug):
    if debug:
        set_logger(lg, logging.DEBUG)


@cli.command(help='echo')
@click.option('-s', '--size', default=10, help='size of results')
def echo(size):
    print(f'size={size}')


if __name__ == '__main__':
    cli()

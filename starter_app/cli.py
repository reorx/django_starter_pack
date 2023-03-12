import click
import logging

from .utils.django_integration import setup_starter_app

setup_starter_app()

from .log import lg, set_logger
from .contact.models import Contact  # noqa




@click.group()
@click.option('-d', '--debug', is_flag=True)
def cli(debug):
    if debug:
        set_logger(lg, logging.DEBUG)


@cli.command(help='list and show contacts')
@click.option('-s', '--size', default=10, help='size of results')
def list_contacts(size):
    for i in Contact.objects.all()[:size]:
        print(f'{i.id}: {i.name}\t{i.created_at}')


@cli.command(help='show single contact by id')
@click.argument('contact_id', type=click.INT, nargs=1)
def show_contact(contact_id):
    i = Contact.objects.get(id=contact_id)
    print(f'{i.id}: {i.name}\t{i.created_at}')


if __name__ == '__main__':
    cli()

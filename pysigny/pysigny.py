import click
import pathlib

from .tuf_helpers import default_trust_dir, init_repo

global_options = [
    click.option('--trustdir', default=default_trust_dir,
                 help='Directory where the trust data is persisted', show_default=True)
]


def apply_global_options(func):
    for option in global_options:
        func = option(func)
    return func


@click.group()
def cli():
    """PySigny is a Python implementation of the CNAB Security Specification."""
    pass


@apply_global_options
@click.command()
@click.argument('target')
@click.argument('name')
def sign(target, name, trustdir):
    """Initializes a new trust collection."""

    click.echo('Signing file {0} and adding to repo {1} in trust dir {2}'.format(
        target, name, trustdir))

    init_repo(target, name, trustdir)


cli.add_command(sign)

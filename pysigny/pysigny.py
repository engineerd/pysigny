import click
import pathlib

from .helper import DEFAULT_TRUST_DIR, init_repo

global_options = (
    click.option('--trustdir', default=DEFAULT_TRUST_DIR,
                 help='Directory where the trust data is persisted', show_default=True),
)


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
@click.argument('repo_name')
def init(repo_name, trustdir):
    """Initializes a new trust collection."""

    click.echo('Init repo {repo_name} in trust dir {trustdir}')

    init_repo(trustdir, repo_name)


cli.add_command(init)

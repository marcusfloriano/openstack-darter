
import click

from darter.commands import commands
from darter.config import DarterConfig


@click.command(cls=click.CommandCollection, sources=[commands])
@click.pass_context
def cli(ctx):
    '''Openstack Darter this for CLI for generate info about capacity'''
    ctx.obj = DarterConfig()


if __name__ == '__main__':
    cli()



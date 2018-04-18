import click

from darter.commands import *


@click.group()
@click.pass_context
def cli(ctx):
    '''Openstack Darter this for CLI for generate info about capacity'''


cli.add_command(totals)



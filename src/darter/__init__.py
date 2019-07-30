# -*- coding: utf-8 -*-
import click

from darter.util import DarterUtil
from darter.commands.domain_commands import domain
from darter.commands.project_commands import project
from darter.commands.capacity_commands import capacity
from darter.commands.hypervisor_commands import hypervisor


@click.command(cls=click.CommandCollection, sources=[domain, project, capacity, hypervisor])
@click.pass_context
def cli(ctx):

    """Openstack Darter this for CLI for generate info about capacity"""

    ctx.obj = DarterUtil()


if __name__ == '__main__':
    cli()



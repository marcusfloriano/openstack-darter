# -*- coding: utf-8 -*-
import click

from darter.commands.hypervisor_commands import sync as hypervisor_sync
from darter.commands.domain_commands import sync as domain_sync
from darter.commands.project_commands import sync as project_sync


@click.group()
def main():
    pass


@main.command("sync")
@click.option('--region', required=True, type=str)
@click.pass_context
def sync(ctx, region):
    """Sync is for get all info by region"""
    ctx.obj.init_logger(__name__)
    ctx.obj.get_logger().debug("Start sync on region")

    ctx.forward(hypervisor_sync)
    ctx.invoke(hypervisor_sync, region)

    ctx.forward(domain_sync)
    ctx.invoke(domain_sync, region)

    ctx.forward(project_sync)
    ctx.invoke(project_sync, region)

    ctx.obj.get_logger().debug("End sync on region")


# -*- coding: utf-8 -*-
import click
import logging

from darter.exceptions import DarterException
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
    logger = logging.getLogger(__name__)
    logger.debug("Start sync on region: %s" % region)

    try:
        ctx.forward(hypervisor_sync)
        ctx.forward(domain_sync)
        ctx.forward(project_sync)
    except DarterException as e:
        logger.error(e)

    logger.debug("End sync on region: %s" % region)


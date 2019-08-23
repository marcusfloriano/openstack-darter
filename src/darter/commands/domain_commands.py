# -*- coding: utf-8 -*-
import click
import logging

from terminaltables import AsciiTable
from darter.models import Domain
from darter.exceptions import DarterException


@click.group()
def domain():
    pass


@domain.command("domains-sync")
@click.pass_obj
@click.option('--region', required=True, type=str)
def sync(util, region):
    """Get all Domains from openstack"""
    logger = logging.getLogger(__name__)
    logger.debug("Start executing domains")

    try:
        util.get_redis_queue().enqueue("darter.jobs.get_all_domains", region)
    except DarterException as e:
        logger.error(e)

    logger.debug("End executing domains")


@domain.command("domains")
@click.pass_obj
@click.option('--region', required=True, type=str)
def domains_list(util, region):
    """List all domains from region"""
    logger = logging.getLogger(__name__)
    logger.debug("Start executing domains_list")

    data = [['ID', 'Name']]
    for d in Domain().find_all(region):
        data.append([d.uuid, d.name])

    table = AsciiTable(data)
    click.echo(table.table)

    logger.debug("End executing domains_list")


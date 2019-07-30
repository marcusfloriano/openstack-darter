# -*- coding: utf-8 -*-
import click

from terminaltables import AsciiTable
from darter.models import Domain


@click.group()
def domain():
    pass


@domain.command("domains-sync")
@click.pass_obj
@click.option('--region', required=True, type=str)
def sync(util, region):
    """Get all Domains from openstack"""
    util.init_logger(__name__)
    util.get_logger().debug("Start executing domains")

    util.get_redis_queue().enqueue("darter.jobs.get_all_domains", region)

    util.get_logger().debug("End executing domains")


@domain.command("domains")
@click.pass_obj
@click.option('--region', required=True, type=str)
def domains_list(util, region):
    """List all domains from region"""
    util.init_logger(__name__)
    util.get_logger().debug("Start executing domains_list")

    data = [['ID', 'Name']]
    for d in Domain().find_all(region):
        data.append([d.uuid, d.name])

    table = AsciiTable(data)
    click.echo(table.table)

    util.get_logger().debug("End executing domains_list")


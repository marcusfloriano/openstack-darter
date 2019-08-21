# -*- coding: utf-8 -*-
import click

from darter.exceptions import DarterException

@click.group()
def hypervisor():
    pass


@hypervisor.command("hypervisors-sync")
@click.pass_obj
@click.option('--region', required=True, type=str)
def sync(util, region):
    """Get Hypervisors from openstack"""
    util.init_logger(__name__)
    util.get_logger().debug("Start executing hypervisors")

    try:
        util.get_redis_queue().enqueue("darter.jobs.get_hypervisors", region)
    except DarterException as e:
        util.get_logger().error(e)

    util.get_logger().debug("End executing hypervisors")


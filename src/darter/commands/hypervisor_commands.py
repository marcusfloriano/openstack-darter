# -*- coding: utf-8 -*-
import click
import logging

from darter.exceptions import DarterException


@click.group()
def hypervisor():
    pass


@hypervisor.command("hypervisors-sync")
@click.pass_obj
@click.option('--region', required=True, type=str)
def sync(util, region):
    """Get Hypervisors from openstack"""
    logger = logging.getLogger(__name__)
    logger.debug("Start executing hypervisors")

    try:
        util.get_redis_queue().enqueue("darter.jobs.get_hypervisors", region)
    except DarterException as e:
        logger.error(e)

    logger.debug("End executing hypervisors")


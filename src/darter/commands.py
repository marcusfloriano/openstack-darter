# -*- coding: utf-8 -*-
import click


@click.group()
def commands():
    pass


@commands.command()
@click.pass_obj
@click.option('--region', required=True, type=str)
def domains(util, region):
    """Get all Domains from openstack"""
    util.init_logger(__name__)
    util.get_logger().debug("Start executing domains")

    util.get_redis_queue().enqueue("darter.jobs.get_all_domains", region)

    util.get_logger().debug("End executing domains")


@commands.command()
@click.pass_obj
@click.option('--region', required=True, type=str)
def projects(util, region):
    """Get all projects from each Domain"""
    util.init_logger(__name__)
    util.get_logger().debug("Start executing projects")

    util.get_redis_queue().enqueue("darter.jobs.queue_all_projects", region)

    util.get_logger().debug("End executing projects")


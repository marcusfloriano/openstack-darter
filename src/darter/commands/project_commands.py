# -*- coding: utf-8 -*-
import click
import json

from terminaltables import AsciiTable
from darter.models import Project


@click.group()
def project():
    pass


@project.command("projects-sync")
@click.pass_obj
@click.option('--region', required=True, type=str)
def sync(util, region):
    """Get all projects from each Domain"""
    util.init_logger(__name__)
    util.get_logger().debug("Start executing projects")

    util.get_redis_queue().enqueue("darter.jobs.queue_all_projects", region)

    util.get_logger().debug("End executing projects")


@project.command("projects")
@click.pass_obj
@click.option('--domain-id', required=True, type=str)
@click.option('--region', required=True, type=str)
def project_list(util, domain_id, region):
    """List all projects from domain"""
    """Get all projects from each Domain"""
    util.init_logger(__name__)
    util.get_logger().debug("Start executing projects list")

    data = [['ID', 'Name']]
    for p in Project().find_all(domain_id, region):
        data.append([p.uuid, p.name])

    table = AsciiTable(data)
    click.echo(table.table)

    util.get_logger().debug("End executing projects list")


@project.command("project-info")
@click.pass_obj
@click.option('--domain-id', required=True, type=str)
@click.option('--project-id', required=True, type=str)
@click.option('--region', required=True, type=str)
def project_info(util, domain_id, project_id, region):
    """List all projects from domain"""
    """Get all projects from each Domain"""
    util.init_logger(__name__)
    util.get_logger().debug("Start executing projects")

    project = Project().find_by_id(domain_id, project_id, region)

    click.echo(json.dumps(project.volume_quotes, indent=4))
    click.echo(json.dumps(project.compute_quotes, indent=4))

    util.get_logger().debug("End executing projects")

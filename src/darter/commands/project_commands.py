# -*- coding: utf-8 -*-
import click
import json
import logging

from terminaltables import AsciiTable
from darter.models import Project
from darter.exceptions import DarterException


@click.group()
def project():
    pass


@project.command("projects-sync")
@click.pass_obj
@click.option('--region', required=True, type=str)
def sync(util, region):
    """Get all projects from each Domain"""
    logger = logging.getLogger(__name__)
    logger.debug("Start executing projects")

    try:
        util.get_redis_queue().enqueue("darter.jobs.queue_all_projects", region)
    except DarterException as e:
        logger.error(e)

    logger.debug("End executing projects")


@project.command("projects")
@click.pass_obj
@click.option('--domain-id', required=True, type=str)
@click.option('--region', required=True, type=str)
def project_list(util, domain_id, region):
    """List all projects from domain"""
    """Get all projects from each Domain"""
    logger = logging.getLogger(__name__)
    logger.debug("Start executing projects list")

    data = [['ID', 'Name']]
    for p in Project().find_all(domain_id, region):
        data.append([p.uuid, p.name])

    table = AsciiTable(data)
    click.echo(table.table)

    logger.debug("End executing projects list")


@project.command("project-info")
@click.pass_obj
@click.option('--domain-id', required=True, type=str)
@click.option('--project-id', required=True, type=str)
@click.option('--region', required=True, type=str)
def project_info(util, domain_id, project_id, region):
    """List all projects from domain"""
    """Get all projects from each Domain"""
    logger = logging.getLogger(__name__)
    logger.debug("Start executing projects")

    project = Project().find_by_id(domain_id, project_id, region)

    click.echo(json.dumps(project.volume_quotes, indent=4))
    click.echo(json.dumps(project.compute_quotes, indent=4))

    logger.debug("End executing projects")

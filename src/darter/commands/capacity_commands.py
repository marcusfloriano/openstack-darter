# -*- coding: utf-8 -*-
import click

from terminaltables import AsciiTable
from darter.models import Project, Domain


@click.group()
def capacity():
    pass


@capacity.command("capacity")
@click.pass_obj
@click.option('--region', required=True, type=str)
def resume(util, region):
    util.init_logger(__name__)
    util.get_logger().debug("Start executing capacity resume")

    domains = Domain().find_all(region, True)

    cpu_used = 0
    gb_used = 0
    total_instances_used = 0
    for d in domains:
        projects = Project().find_all(d.uuid, region)
        data = [['Field', 'Value']]
        for p in projects:
            if 'totalGigabytesUsed' in p.volume_quotes and p.volume_quotes['totalGigabytesUsed'] > 0:
                db_used = db_used + p.volume_quotes['totalGigabytesUsed']
            cpu_used = cpu_used + p.compute_quotes['total_cores_used']
            total_instances_used = total_instances_used + p.compute_quotes['total_instances_used']

    data = [['Fields', 'Name']]

    data.append(['CPU', cpu_used])
    data.append(['Instaces', total_instances_used])

    table = AsciiTable(data)
    click.echo(table.table)

# -*- coding: utf-8 -*-
import click

from terminaltables import AsciiTable
from darter.models import Project, Domain, Hypervisor
from darter.openstack_util import OpenstackUtil


@click.group()
def capacity():
    pass


@capacity.command("capacity")
@click.pass_obj
@click.option('--region', required=True, type=str)
def resume(util, region):
    util.init_logger(__name__)
    util.get_logger().debug("Start executing capacity resume")

    hypervisors = Hypervisor().find_all(region)
    data = {
        'vcpus_used': 0,
        'memory_used': 0,
        'total_instances_used': 0
    }
    for h in hypervisors:
        data['vcpus_used'] = data['vcpus_used'] + h.vcpus_used
        data['memory_used'] = data['memory_used'] + h.memory_used

    domains = Domain().find_all(region, True)

    for d in domains:
        projects = Project().find_all(d.uuid, region)
        for p in projects:
            data['total_instances_used'] = data['total_instances_used'] + p.compute_quotes['total_instances_used']

    data['memory_used'] = int(data['memory_used'] / 1024)
    print(data)

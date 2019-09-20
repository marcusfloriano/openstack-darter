# -*- coding: utf-8 -*-
"""Contains commands for generate views of capacities"""
import click
import logging

from darter.models import Project, Domain, Hypervisor, JsonWriter
from darter.views import HypervisorView, DomainView, ProjectView


@click.group()
def capacity():
    pass


@capacity.command("capacity")
@click.pass_obj
@click.option('--region', required=True, type=str)
def resume(util, region):
    """Command for generate resume of capacity by region

    Args:
        util (pass_obj): Object UTIL passed from @click.pass_object
        region (str): Region for generate resume

    """
    logger = logging.getLogger(__name__)
    logger.debug("Start executing capacity resume")

    keys_volume_in_use_show = []
    darter_config = util.get_config("darter")
    if 'cinder_keys_show' in darter_config:
        keys_volume_in_use_show = darter_config['cinder_keys_show']

    hypervisors = HypervisorView().find_all(region)
    data = {
        'vcpus_used': 0,
        'memory_used': 0,
        'vcpus_size': 0,
        'memory_size': 0,
        'servers_total': 0,
        'cinder': {}
    }
    for h in hypervisors:
        data['vcpus_used'] = data['vcpus_used'] + h.vcpus_used
        data['memory_used'] = data['memory_used'] + h.memory_used
        data['vcpus_size'] = data['vcpus_size'] + h.vcpus_size
        data['memory_size'] = data['memory_size'] + h.memory_size

    domains = DomainView().find_all(region, True)

    for d in domains:
        projects = ProjectView().find_all(d.uuid, region)
        for p in projects:
            data['servers_total'] = data['servers_total'] + len(p.servers_ids)
            for k in p.volume_quotes.keys():
                if len(keys_volume_in_use_show) > 0 and k not in keys_volume_in_use_show:
                    continue
                if k not in data['cinder']:
                    data['cinder'][k] = {
                        'in_use': 0,
                        'limit': 0
                    }
                data['cinder'][k]['in_use'] = data['cinder'][k]['in_use'] + p.volume_quotes[k]['in_use']
                print(p.volume_quotes[k])
                data['cinder'][k]['limit'] = data['cinder'][k]['limit'] + int(p.volume_quotes[k]['limit'])

    data['memory_used'] = int(data['memory_used'] / 1024)
    JsonWriter().write("capacity-resume-%s" % region, "capacity", {"%s" % region: data})

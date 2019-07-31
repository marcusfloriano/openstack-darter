# -*- coding: utf-8 -*-
import json

from darter.util import DarterUtil
from darter.openstack_util import OpenstackUtil
from darter.models import JsonWriter, Domain, Project

darter_util = DarterUtil()
darter_util.init_logger(__name__)


def get_hypervisors(region):
    """Job for get hypervisor infos"""
    darter_util.get_logger().debug("Start processing get_hypervisors")
    hypervisors = OpenstackUtil(region).get_hypervisors()
    JsonWriter().write("hypervisors-%s" % region, "hypervisors", hypervisors)
    darter_util.get_logger().debug("End processing get_hypervisors")


def get_all_domains(region):
    """Job for get all domains from openstack"""
    darter_util.get_logger().debug("Start processing job_get_domains")
    domains = OpenstackUtil(region).get_domains()
    darter_util.get_logger().debug("Region: %s" % region)
    darter_util.get_logger().debug("Domains total: %s" % len(domains))
    JsonWriter().write("domains-%s" % region, "domains", domains)
    darter_util.get_logger().debug("End processing job_get_domains")


def queue_all_projects(region):
    darter_util.get_logger().debug("Start processing projects_processing")
    darter_config = darter_util.get_config("darter")
    with open("%s/%s.json" % (darter_config['datafiles'], 'domains-%s' % region)) as json_file:
        data = json.load(json_file)
        for _domain in data['domains']:
            domain = Domain().from_json(_domain)
            darter_util.get_redis_queue().enqueue("darter.jobs.get_projects_by_domain", region, domain)
            darter_util.get_redis_queue().enqueue("darter.jobs.get_total_servers", region, domain)
    darter_util.get_logger().debug("End processing projects_processing")


def get_projects_by_domain(region: str, domain: Domain):
    """Get all projects from Domain by Domain Object"""
    darter_util.get_logger().debug("Start processing get_projects_by_domain")
    darter_util.get_logger().debug("Region: %s" % region)
    darter_util.get_logger().debug(domain.to_json())
    projects = OpenstackUtil(region).get_projects(domain.uuid)

    JsonWriter("domain/%s" % region).write("domain-%s" % domain.uuid, "projects", projects)
    darter_util.get_logger().debug("End processing get_projects_by_domain")


def get_total_servers(region: str, domain: Domain):
    darter_util.get_logger().debug("Start processing get_total_servers")
    projects = []
    openstack_util = OpenstackUtil(region)
    for p in Project().find_all(domain.uuid, region):
        p.servers_ids = openstack_util.get_servers_ids(p.uuid)
        projects.append(p.to_json())

    JsonWriter("domain/%s" % region).write("domain-%s" % domain.uuid, "projects", projects)
    darter_util.get_logger().debug("End processing get_total_servers")





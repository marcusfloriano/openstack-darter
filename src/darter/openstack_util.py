# -*- coding: utf-8 -*-
import openstack.cloud

from darter.models import Domain, Project, Hypervisor
from darter.util import DarterUtil

'''This class is for calculate the measurement for items into openstack '''


class OpenstackUtil:

    def __init__(self, region):
        self.region = region
        self.conn = openstack.connect(cloud=self.region)
        self.darter_util = DarterUtil()
        self.darter_util.init_logger(__name__)

    def get_hypervisors(self):
        hypervisors = []
        for h in self.conn.list_hypervisors():
            hypervisors.append(Hypervisor(h['id'], h['vcpus_used'], h['memory_used']).to_json())
        return hypervisors

    def get_domains(self):
        domains = []
        for domain in self.conn.identity.domains():
            d = Domain(domain.id, domain.name, self.region)
            domains.append(d.to_json())
        return domains

    def get_projects(self, domain_id):
        projects = []
        for project in self.conn.identity.projects(domain_id=domain_id):
            servers = self.conn.list_servers(False, True, filters={"project_id": project.id})
            p = Project(project.id, project.name, domain_id)
            p = self.get_compute_totals(p)
            p.servers = len(servers)
            projects.append(p.to_json())
        return projects

    def get_compute_totals(self, project: Project):
        self.darter_util.get_logger().debug("get_compute_totals for %s" % project.name)
        quota = self.conn.get_compute_limits(name_or_id=project.uuid)

        project.compute_quotes = {
            'total_cores_used': quota.total_cores_used,
            'total_instances_used': quota.total_instances_used,
            'total_ram_used': quota.total_ram_used,
            'max_total_cores': quota.max_total_cores,
            'max_total_instances': quota.max_total_instances,
            'max_total_instances': quota.max_total_ram_size,
        }

        self.darter_util.get_logger().debug("get_volume_quotas for %s" % project.name)
        quota_volume = self.conn.get_volume_limits(name_or_id=project.uuid)
        self.darter_util.get_logger().debug(quota_volume)
        for v in quota_volume:
            project.volume_quotes[v] = quota_volume[v]

        return project


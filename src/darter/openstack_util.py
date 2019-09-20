# -*- coding: utf-8 -*-
import openstack.cloud
import logging
import json

from darter.models import Domain, Project, Hypervisor
from darter.util import DarterUtil
from cinderclient.v2 import client as cinderclient
from cinderclient import utils

'''This class is for calculate the measurement for items into openstack '''

_quota_resources = ['volumes', 'snapshots', 'gigabytes',
                    'backups', 'backup_gigabytes',
                    'per_volume_gigabytes', 'groups', ]


class OpenstackUtil:

    def __init__(self, region):
        self.region = region
        self.conn = openstack.connect(cloud=self.region)
        self.conn_cinder = cinderclient.Client(session=self.conn.session)
        self.darter_util = DarterUtil()
        self.logger = logging.getLogger(__name__)

    def get_hypervisors(self):
        hypervisors = []
        for h in self.conn.list_hypervisors():
            self.logger.debug(json.dumps(h, indent=4))
            hypervisors.append(Hypervisor(h['id'], h['vcpus_used'], h['memory_used'], h['vcpus'], h['memory_size']).to_json())
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
            p = Project(project.id, project.name, domain_id)
            p = self.get_compute_totals(p)
            projects.append(p.to_json())
        return projects

    def get_servers_ids(self, project_id):
        servers = self.conn.list_servers(False, True, filters={"project_id": project_id})
        ids = []
        for s in servers:
            ids.append(s['id'])
        return ids

    def get_compute_totals(self, project: Project):
        self.logger.debug("get_compute_totals for %s" % project.name)
        quota = self.conn.get_compute_limits(name_or_id=project.uuid)
        self.logger.debug(json.dumps(quota, indent=4))
        project.compute_quotes = {
            'total_cores_used': quota.total_cores_used,
            'total_instances_used': quota.total_instances_used,
            'total_ram_used': quota.total_ram_used,
            'max_total_cores': quota.max_total_cores,
            'max_total_instances': quota.max_total_instances,
            'max_total_ram_size': quota.max_total_ram_size
        }

        self.logger.debug("get_volume_quotas for %s" % project.name)
        quota_volume = self.conn_cinder.quotas.get(project.uuid, True)
        self.logger.debug(quota_volume)
        for q in self.quota_usage_show(quota_volume):
            project.volume_quotes[q['Type']] = {
                'limit': q['Limit'],
                'in_use': q['In_use']
            }
        return project

    def quota_usage_show(self, quotas):
        quota_list = []
        quotas_info_dict = utils.unicode_key_value_to_string(quotas._info)
        for resource in quotas_info_dict.keys():
            good_name = False
            for name in _quota_resources:
                if resource.startswith(name):
                    good_name = True
            if not good_name:
                continue
            quota_info = getattr(quotas, resource, None)
            quota_info['Type'] = resource
            quota_info = dict((k.capitalize(), v) for k, v in quota_info.items())
            quota_list.append(quota_info)
        return quota_list

# -*- coding: utf-8 -*-
import re
import os

from darter.models import JsonReader, Domain, Project, Hypervisor
from darter.util import DarterUtil


class DomainView:

    def find_all(self, region, all=False):
        items = JsonReader().reader("domains-%s" % region, "domains")

        project_view = ProjectView()

        domains = []
        for item in items:
            d = Domain().from_json(item)
            projects = project_view.find_all(d.uuid, region)
            if all:
                domains.append(Domain().from_json(item))
            else:
                for p in projects:
                    if 'totalGigabytesUsed' in p.volume_quotes and p.volume_quotes['totalGigabytesUsed'] > 0:
                        domains.append(Domain().from_json(item))
                        break
                    elif 'total_cores_used' in p.compute_quotes and p.compute_quotes['total_cores_used'] > 0:
                        domains.append(Domain().from_json(item))
                        break

        def _sort(e):
            return e.name

        domains.sort(key=_sort)
        return domains


class ProjectView:

    def find_all(self, domain_uuid, region):
        items = JsonReader("domain/%s" % region).reader("domain-%s" % domain_uuid, "projects")
        projects = []
        for item in items:
            projects.append(Project().from_json(item))

        def _sort(e):
            return e.name

        projects.sort(key=_sort)
        return projects

    def find_by_id(self, domain_uuid, project_uuid, region):
        projects = self.find_all(domain_uuid, region)
        for p in projects:
            if p.uuid == project_uuid:
                return p
        return None


class HypervisorView:

    def find_all(self, region):
        items = JsonReader().reader("hypervisors-%s" % region, "hypervisors")
        hypervisors = []
        for item in items:
            hypervisors.append(Hypervisor().from_json(item))

        def _sort(e):
            return e.uuid

        hypervisors.sort(key=_sort)
        return hypervisors


class CapacityView:

    def __init__(self):
        self.util = DarterUtil()
        self.data_store = self.util.get_store_data()

    def find_all(self):
        data = {}
        for file in os.listdir(self.data_store):
            if re.match("^capacity\-resume\-.*?\.json$", file):
                content = JsonReader().reader(file.replace(".json", ""), 'capacity')
                data.update(content)
        return data
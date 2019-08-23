# -*- coding: utf-8 -*-
"""Models

This module contains all structs that used on Openstack-Darter.

"""
import os
import json
import logging

from darter.util import DarterUtil
from pathlib import Path


class Domain:

    """ Domain is one unique domain.

    Attributes:
        uuid (string): UUID of the domain
        name (string): Name of the domain
        region (string): Name of Region

    """
    def __init__(self, uuid=None, name=None, region=None):
        self.uuid = uuid
        self.name = name
        self.region = region

    def find_all(self, region, all=False):
        items = JsonReader().reader("domains-%s" % region, "domains")
        domains = []
        for item in items:
            d = Domain().from_json(item)
            projects = Project().find_all(d.uuid, region)
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

    def to_json(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'region': self.region
        }

    def from_json(self, data):
        self.uuid = data['uuid']
        self.name = data['name']
        self.region = data['region']
        return self


class Project:

    """ Project is unique project from domain.

    Attributes:
        uuid (string): UUID of the project on domain
        name (string): Name of the project
        domain_id (string): Domain UUID
        compute_quotes

    """

    def __init__(self, uuid=None, name=None, domain_id=None):
        self.uuid = uuid
        self.name = name
        self.domain_id = domain_id
        self.compute_quotes = {}
        self.volume_quotes = {}
        self.servers_ids = []

    def find_all(self, domain_uuid, region):
        # items = JsonReader("domain/%s" % region).reader("domain-%s" % domain_uuid, "projects")
        projects = []
        # project = Project()
        # for item in items:
        #     projects.append(project.from_json(item))

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

    def to_json(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'domain_id': self.domain_id,
            'compute_quotes': self.compute_quotes,
            'volume_quotes': self.volume_quotes,
            'servers_ids': self.servers_ids
        }

    def from_json(self, data):
        self.uuid = data['uuid']
        self.name = data['name']
        self.domain_id = data['domain_id']
        self.compute_quotes = data['compute_quotes']
        self.volume_quotes = data['volume_quotes']
        self.servers_ids = data['servers_ids']
        return self


class Hypervisor:

    """ Hypervisor is contains information the memory and vCPUs is used

    Attributes:
        uuid (string): ID hypervisor
        vcpus_used (int): vCPUs used by hypervisor
        memory_used (int): memory used by hypervisor
    """

    def __init__(self, uuid=None, vcpus_used=None, memory_used=None):
        self.uuid = uuid
        self.vcpus_used = vcpus_used
        self.memory_used = memory_used

    def find_all(self, region):
        items = JsonReader().reader("hypervisors-%s" % region, "hypervisors")
        hypervisors = []
        for item in items:
            hypervisors.append(Hypervisor().from_json(item))

        def _sort(e):
            return e.uuid

        hypervisors.sort(key=_sort)
        return hypervisors

    def to_json(self):
        return {
            'uuid': self.uuid,
            'vcpus_used': self.vcpus_used,
            'memory_used': self.memory_used
        }

    def from_json(self, data):
        self.uuid = data['uuid']
        self.vcpus_used = data['vcpus_used']
        self.memory_used = data['memory_used']
        return self


class DarterReaderWriter:

    def __init__(self, path=None):
        self.util = DarterUtil()
        self.logger = logging.getLogger(__name__)
        self.datafiles = self.util.get_store_data()
        if path is not None:
            self.datafiles = "%s/%s" % (self.datafiles, path)
        if not Path("%s" % self.datafiles).is_dir():
            self.logger.debug("Create directory data files: %s" % self.datafiles)
            os.makedirs("%s" % self.datafiles)


class JsonWriter(DarterReaderWriter):

    """JsonWrite is to create json structs files"""

    def write(self, file, name, items):
        self.logger.debug("Writer '%s' in file '%s'" % (name, file))
        data = {
            'totals': len(items),
            name: items
        }
        # self.logger.debug("Writer data '%s' in file '%s'" % (data, ("%s/%s.json" % (self.datafiles, file))))
        with open("%s/%s.json" % (self.datafiles, file), 'w') as file:
            json.dump(data, file)


class JsonReader(DarterReaderWriter):

    """JsonReader is to reader json structs files"""

    def reader(self, file, name):
        with open("%s/%s.json" % (self.datafiles, file), 'r') as file:
            data = json.load(file)
            return data[name]

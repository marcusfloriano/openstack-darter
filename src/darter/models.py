# -*- coding: utf-8 -*-
"""Models

This module contains all structs that used on Openstack-Darter.

"""
import os
import json
import logging
import re

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

    def __init__(self, uuid=None, vcpus_used=None, memory_used=None, vcpus_size=None, memory_size=None):
        self.uuid = uuid
        self.vcpus_used = vcpus_used
        self.memory_used = memory_used
        self.vcpus_size = vcpus_size
        self.memory_size = memory_size

    def to_json(self):
        return {
            'uuid': self.uuid,
            'vcpus_used': self.vcpus_used,
            'memory_used': self.memory_used,
            'vcpus_size': self.vcpus_size,
            'memory_size': self.memory_size
        }

    def from_json(self, data):
        self.uuid = data['uuid']
        self.vcpus_used = data['vcpus_used']
        self.memory_used = data['memory_used']
        self.vcpus_size = data['vcpus_size']
        self.memory_size = data['memory_size']
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
        self.logger.debug("%s/%s.json" % (self.datafiles, file))
        with open("%s/%s.json" % (self.datafiles, file), 'r') as file:
            data = json.load(file)
            return data[name]

# -*- coding: utf-8 -*-
"""Models

This module contains all structs that used on Openstack-Darter.

"""
import os
import json

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
        total_cores_used
        total_instances_used
        total_ram_used
        max_total_cores
        max_total_instances
        max_total_ram_size

    """

    def __init__(self, uuid, name, domain_id):
        self.uuid = uuid
        self.name = name
        self.domain_id = domain_id
        self.total_cores_used = None
        self.total_instances_used = None
        self.total_ram_used = None
        self.max_total_cores = None
        self.max_total_instances = None
        self.max_total_ram_size = None

    def to_json(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'domain_id': self.domain_id,
            'total_cores_used': self.total_cores_used,
            'total_instances_used': self.total_instances_used,
            'total_ram_used': self.total_ram_used,
            'max_total_cores': self.max_total_cores,
            'max_total_instances': self.max_total_instances,
            'max_total_ram_size': self.max_total_ram_size
        }

    def from_json(self, data):
        self.uuid = data['uuid']
        self.name = data['name']
        self.domain_id = data['domain_id']
        self.total_cores_used = data['total_cores_used']
        self.total_instances_used = data['total_instances_used']
        self.total_ram_used = data['total_ram_used']
        self.max_total_cores = data['max_total_cores']
        self.max_total_instances = data['max_total_instances']
        self.max_total_ram_size = data['max_total_ram_size =']
        return self


class JsonWriter:

    """JsonWrite is to create json structs files"""

    def __init__(self, path=None):
        darter_config = DarterUtil().get_config("darter")
        self.datafiles = darter_config['datafiles']
        if path is not None:
            self.datafiles = "%s/%s" % (self.datafiles, path)
        if not Path("%s" % self.datafiles).is_dir():
            os.makedirs("%s" % self.datafiles)

    def items(self, file, name, items):
        data = {
            'totals': len(items),
            name: items
        }
        with open("%s/%s.json" % (self.datafiles, file), 'w') as file:
            json.dump(data, file)

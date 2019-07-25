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
        compute_quotes

    """

    def __init__(self, uuid, name, domain_id):
        self.uuid = uuid
        self.name = name
        self.domain_id = domain_id
        self.compute_quotes = {}

    def to_json(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'domain_id': self.domain_id,
            'compute_quotes': self.compute_quotes
        }

    def from_json(self, data):
        self.uuid = data['uuid']
        self.name = data['name']
        self.domain_id = data['domain_id']
        self.compute_quotes = data['compute_quotes']
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

    def write(self, file, name, items):
        data = {
            'totals': len(items),
            name: items
        }
        with open("%s/%s.json" % (self.datafiles, file), 'w') as file:
            json.dump(data, file)

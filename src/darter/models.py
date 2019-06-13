# -*- coding: utf-8 -*-
"""Models

This module contains all structs that used on Openstack-Darter.

"""
import os
import json

from darter.config import DarterConfig
from pathlib import Path


class Domain:

    """ Domain is one unique domain.

    Attributes:
        uuid (string): UUID of the domain
        name (string): Name of the domain
        region (string): Name of Region

    """
    def __init__(self, uuid, name, region):
        self.uuid = uuid
        self.name = name
        self.region = region

    def to_json(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'region': self.region
        }


class Project:

    """ Project is unique project from domain.

    Attributes:
        uuid (string): UUID of the project on domain
        name (string): Name of the project
        domain_id (string): Domain UUID
    """
    def __init__(self, uuid, name, domain_id):
        self.uuid = uuid
        self.name = name
        self.domain_id = domain_id


class JsonWriter:

    """JsonWrite is to create json strutcs files"""

    def __init__(self):
        darter_config = DarterConfig().get("darter")
        self.datafiles = darter_config['datafiles']
        if not Path("%s" % self.datafiles).is_dir():
            os.makedirs("%s" % self.datafiles)

    def items(self, file, name, items):
        data = {
            'totals': len(items),
            name: items
        }
        with open("%s/%s.json" % (self.datafiles, file), 'w') as file:
            json.dump(data, file)

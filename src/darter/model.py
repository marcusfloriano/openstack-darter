# -*- coding: utf-8 -*-
"""Models

This module contains all structs that used on Openstack-Darter.

"""


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

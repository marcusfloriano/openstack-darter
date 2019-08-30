# -*- coding: utf-8 -*-
import click
import os
import yaml
import logging
import logging.config
import re

from pathlib import Path
from darter.exceptions import DarterException
from darter.util import DarterUtil
from darter.commands.domain_commands import domain
from darter.commands.project_commands import project
from darter.commands.capacity_commands import capacity
from darter.commands.hypervisor_commands import hypervisor
from darter.commands.main_commands import main
from darter.commands.web_commands import web


UNIX_CONFIG_HOME = os.path.join(os.path.expanduser(os.path.join('~', '.config')), 'darter')
UNIX_SITE_CONFIG_HOME = '/etc/darter'


CONFIG_SEARCH_PATH = [
    os.getcwd(),
    UNIX_CONFIG_HOME, UNIX_SITE_CONFIG_HOME
]


YAML_SUFFIXES = ('.yaml', '.yml')


CONFIG_FILES = [
    os.path.join(d, 'darter' + s)
    for d in CONFIG_SEARCH_PATH
    for s in YAML_SUFFIXES
]


def get_config():
    for path in CONFIG_FILES:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return path, yaml.safe_load(f)
    raise DarterException("Not load the config file, verify if files exists in %s." % CONFIG_FILES)


config_filename, config = get_config()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG if config['debug'] else logging.INFO,
            'formatter': 'simple'
        },
    },
    'loggers': {
        'darter': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'rq': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

logging.config.dictConfig(LOGGING)


def get_store_data():
    store_data = re.sub(r'(.*\/).*', '\g<1>', config_filename) if config_filename is not None else None
    datafiles = "%s/data" % store_data
    datafiles = datafiles.replace("//", "/")
    if not Path("%s" % datafiles).is_dir():
        os.makedirs("%s" % datafiles)
    return datafiles


store_data_dir = get_store_data()


@click.command(cls=click.CommandCollection, sources=[domain, project, capacity, hypervisor, main, web])
@click.pass_context
def cli(ctx):

    """Openstack Darter this for CLI for generate info about capacity"""

    ctx.obj = DarterUtil()


if __name__ == '__main__':
    cli()



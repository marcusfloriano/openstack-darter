# -*- coding: utf-8 -*-
import os
import yaml
import logging

from redis import Redis, ConnectionPool
from rq import Queue

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


class DarterUtil:

    logger = None

    def __init__(self):
        self.filelist = CONFIG_FILES
        self.config_filename, self.darter_config = self._load_config()

    def get_config(self, key):
        if key in self.darter_config:
            return self.darter_config[key]
        else:
            print("Key for %s config not exists" % self.config_filename)

    def _load_config(self):
        for path in self.filelist:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return path, yaml.safe_load(f)
        return None, {}

    def init_logger(self, name):
        self.logger = logging.getLogger(name)
        ch = logging.StreamHandler()
        if self.get_config("debug"):
            self.logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        return self

    def get_logger(self):
        return self.logger

    def get_redis_queue(self):
        redis_config = self.get_config("redis")
        pool = ConnectionPool(host=redis_config["host"])
        queue = Queue("high", connection=Redis(connection_pool=pool))
        return queue


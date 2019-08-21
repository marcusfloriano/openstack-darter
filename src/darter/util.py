# -*- coding: utf-8 -*-
import os
import yaml
import logging
import re

from redis import Redis, ConnectionPool, Connection, RedisError
from rq import Queue
from pathlib import Path
from darter.exceptions import DarterException

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
        self.init_logger(__name__)
        self.filelist = CONFIG_FILES
        try:
            self.config_filename, self.darter_config = self._load_config()
            self.data_dir = re.sub(r'(.*\/).*', '\g<1>',
                                   self.config_filename) if self.config_filename is not None else None
            self.get_logger().debug("Diretory for log is %s" % self.data_dir)
        except DarterException as e:
            self.get_logger().error(e)

    def get_data_dir(self):
        datafiles = "%s/data" % self.data_dir
        datafiles = datafiles.replace("//", "/")
        self.get_logger().debug("Get datafiles %s" % datafiles)
        if not Path("%s" % datafiles).is_dir():
            os.makedirs("%s" % datafiles)
        return datafiles

    def get_config(self, key):
        try:
            if key in self.darter_config:
                return self.darter_config[key]
            else:
                self.get_logger().error("Key for '%s' config not exists" % self.config_filename)
        except Exception:
            raise DarterException("Don't possible found the config file")

    def _load_config(self):
        for path in self.filelist:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return path, yaml.safe_load(f)
        raise DarterException("Not load the config file, verify if files exists in %s." % self.filelist)

    def init_logger(self, name):
        self.logger = logging.getLogger(name)
        ch = logging.StreamHandler()
        try:
            if self.get_config("debug"):
                self.logger.setLevel(logging.DEBUG)
                ch.setLevel(logging.DEBUG)
        except DarterException:
            pass
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        return self

    def get_logger(self):
        return self.logger

    def get_redis_queue(self):
        redis_config = self.get_config("redis")
        try:
            pool = ConnectionPool(host=redis_config["host"])
            pool.make_connection().connect()
            queue = Queue("high", connection=Redis(connection_pool=pool))
            return queue
        except RedisError as e:
            self.get_logger().exception(e)
            raise DarterException("Not possible connection on Redis")


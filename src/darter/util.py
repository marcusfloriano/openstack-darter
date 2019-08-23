# -*- coding: utf-8 -*-
import logging
import darter

from redis import Redis, ConnectionPool, RedisError
from rq import Queue

from darter.exceptions import DarterException


class DarterUtil:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.config_filename, self.darter_config = darter.get_config()
        except DarterException as e:
            self.logger.error(e)

    def get_store_data(self):
        return darter.get_store_data()

    def get_config(self, key):
        try:
            if key in self.darter_config:
                return self.darter_config[key]
            else:
                self.logger.error("Key for '%s' config not exists" % self.config_filename)
        except Exception:
            raise DarterException("Don't possible found the config file")

    def get_redis_queue(self):
        redis_config = self.get_config("redis")
        try:
            pool = ConnectionPool(host=redis_config["host"])
            pool.make_connection().connect()
            queue = Queue("high", connection=Redis(connection_pool=pool))
            return queue
        except RedisError as e:
            self.logger.exception(e)
            raise DarterException("Not possible connection on Redis")


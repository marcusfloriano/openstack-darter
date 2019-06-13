import click
import sys
import logging

from redis import Redis, ConnectionPool
from rq import Queue

from openstack import utils
utils.enable_logging(debug=False, stream=sys.stdout)


@click.group()
def commands():
    pass


@commands.command()
@click.pass_obj
def totals(config):
    """Processing total of Domains and Projects"""
    logging.debug("Starting executing totals")

    redis_config = config.get("redis")
    pool = ConnectionPool(host=redis_config["host"])
    queue = Queue("high", connection=Redis(connection_pool=pool))

    queue.enqueue("darter.jobs.measure_total_domains_and_project", "packstack")


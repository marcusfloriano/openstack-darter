import click
import sys

from darter.util import DarterUtil
from redis import Redis, ConnectionPool
from rq import Queue

from openstack import utils
utils.enable_logging(debug=False, stream=sys.stdout)


@click.group()
def commands():
    pass


@commands.command()
@click.pass_obj
@click.option('--region', required=True, type=str)
def domains(util, region):
    """Get all Domains from openstack"""
    util.init_logger(__name__)
    util.get_logger().debug("Start executing domains")

    redis_config = util.get_config("redis")
    pool = ConnectionPool(host=redis_config["host"])
    queue = Queue("high", connection=Redis(connection_pool=pool))

    queue.enqueue("darter.jobs.domains_processing", region)

    util.get_logger().debug("End executing domains")


@commands.command()
@click.pass_obj
def totals(config):
    """Processing total of Domains and Projects"""
    darter_util.get_logger().debug("Starting executing totals")

    redis_config = config.get("redis")
    pool = ConnectionPool(host=redis_config["host"])
    queue = Queue("high", connection=Redis(connection_pool=pool))

    queue.enqueue("darter.jobs.measure_total_domains_and_project", "packstack")


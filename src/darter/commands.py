import click
import sys

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

    redis_config = config.get("redis")
    pool = ConnectionPool(host=redis_config["host"])
    queue = Queue("high", connection=Redis(connection_pool=pool))

    queue.enqueue("darter.jobs.measure_total_domains_and_project", "packstack")


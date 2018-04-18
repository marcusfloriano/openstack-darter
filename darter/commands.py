import click
import sys

from redis import Redis, ConnectionPool
from rq import Queue
from darter.config import DarterConfig
from openstack import utils
utils.enable_logging(debug=False, stream=sys.stdout)

redis_config = DarterConfig().get("redis")
pool = ConnectionPool(host=redis_config["host"])
queue = Queue("high", connection=Redis(connection_pool=pool))


@click.command()
@click.pass_context
def totals(ctx):
    '''Processing total of Domains and Projects'''
    queue.enqueue("darter.jobs.measure_total_domains_and_project", "packstack")


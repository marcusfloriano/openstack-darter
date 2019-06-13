
import logging

from darter import DarterConfig
from darter.openstack import Openstack
from darter.models import JsonWriter

from redis import Redis, ConnectionPool
from rq import Queue

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()

if DarterConfig().get("debug"):
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

redis_config = DarterConfig().get("redis")
pool = ConnectionPool(host=redis_config["host"])
queue = Queue("high", connection=Redis(connection_pool=pool))


def measure_total_domains_and_project(cloud):

    logger.debug("measure_total_domains_and_project");

    os = Openstack()
    domains = os.get_domains(cloud)

    JsonWriter().items("domains", "domains", domains)

    # client.write_points(
    #     [{
    #         "measurement": "total_domains",
    #         "tags": {
    #             "region": cloud
    #         },
    #         "fields": {
    #             "value": len(domains)
    #         }
    #     }]
    # )
    #
    # all_projects = []
    # for domain in domains:
    #     projects = os.get_projects(cloud, domain)
    #     for project in projects:
    #         all_projects.append({
    #             "domain": domain,
    #             "project": project
    #         })
    #
    # client.write_points(
    #     [{
    #         "measurement": "total_projects",
    #         "tags": {
    #             "region": cloud
    #         },
    #         "fields": {
    #             "value": len(all_projects)
    #         }
    #     }]
    # )
    #
    # queue.enqueue("darter.jobs.measure_totals_compute", cloud, all_projects)


def measure_totals_compute(cloud, all_projects):

    totals_compute = {
        "total_cores_used": 0,
        "total_instances_used": 0,
        "total_ram_used": 0,
        "max_total_cores": 0,
        "max_total_instances": 0,
        "max_total_ram_size": 0
    }

    os = Openstack()

    for project in all_projects:
        totals = os.get_compute_totals(cloud, project["project"])
        totals_compute = {
            "total_cores_used": totals_compute["total_cores_used"] + totals["total_cores_used"],
            "total_instances_used": totals_compute["total_instances_used"] + totals["total_instances_used"],
            "total_ram_used": totals_compute["total_ram_used"] + totals["total_ram_used"],
            "max_total_cores": totals_compute["max_total_cores"] + totals["max_total_cores"],
            "max_total_instances": totals_compute["max_total_instances"] + totals["max_total_instances"],
            "max_total_ram_size": totals_compute["max_total_ram_size"] + totals["max_total_ram_size"]
        }

    def write_points(measurement, value, tags={}):
        client.write_points(
            [{
                "measurement": measurement,
                "tags": tags,
                "fields": {
                    "value": value
                }
            }]
        )

    write_points("total_cores_used", totals_compute["total_cores_used"])
    write_points("total_instances_used", totals_compute["total_instances_used"])
    write_points("total_ram_used", totals_compute["total_ram_used"])
    write_points("max_total_cores", totals_compute["max_total_cores"])
    write_points("max_total_instances", totals_compute["max_total_instances"])
    write_points("max_total_ram_size", totals_compute["max_total_ram_size"])





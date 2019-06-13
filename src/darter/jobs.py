
from darter.util import DarterUtil
from darter.openstack import Openstack
from darter.models import JsonWriter

from redis import Redis, ConnectionPool
from rq import Queue

darter_util = DarterUtil()
darter_util.init_logger(__name__)

redis_config = darter_util.get_config("redis")
pool = ConnectionPool(host=redis_config["host"])
queue = Queue("high", connection=Redis(connection_pool=pool))


def domains_processing(cloud):
    """Job for get all domains from openstack"""
    darter_util.get_logger().debug("Start processing job_get_domains")
    domains = Openstack(cloud).get_domains()
    JsonWriter().items("domains", "domains", domains)
    darter_util.get_logger().debug("End processing job_get_domains")


def measure_total_domains_and_project(cloud):

    darter_util.get_logger().debug("measure_total_domains_and_project");

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





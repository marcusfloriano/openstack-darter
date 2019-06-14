
import json

from darter.util import DarterUtil
from darter.openstack_util import OpenstackUtil
from darter.models import JsonWriter, Domain

darter_util = DarterUtil()
darter_util.init_logger(__name__)


def get_all_domains(region):
    """Job for get all domains from openstack"""
    darter_util.get_logger().debug("Start processing job_get_domains")
    domains = OpenstackUtil(region).get_domains()
    darter_util.get_logger().debug("Region: %s" % region)
    darter_util.get_logger().debug("Domains total: %s" % len(domains))
    JsonWriter().items("domains", "domains", domains)
    darter_util.get_logger().debug("End processing job_get_domains")


def queue_all_projects(region):
    darter_util.get_logger().debug("Start processing projects_processing")
    darter_config = darter_util.get_config("darter")
    with open("%s/%s.json" % (darter_config['datafiles'], 'domains')) as json_file:
        data = json.load(json_file)
        for _domain in data['domains']:
            domain = Domain().from_json(_domain)
            darter_util.get_redis_queue().enqueue("darter.jobs.get_projects_by_domain", region, domain)
    darter_util.get_logger().debug("End processing projects_processing")


def get_projects_by_domain(region: str, domain: Domain):
    """Get all projects from Domain by Domain Object"""
    darter_util.get_logger().debug("Start processing get_projects_by_domain")
    darter_util.get_logger().debug("Region: %s" % region)
    darter_util.get_logger().debug(domain.to_json())
    projects = OpenstackUtil(region).get_projects(domain.uuid)
    JsonWriter("domain").items("%s" % domain.uuid, "projects", projects)
    darter_util.get_logger().debug("End processing get_projects_by_domain")


def measure_total_domains_and_project(cloud):

    darter_util.get_logger().debug("measure_total_domains_and_project");

    os = OpenstackUtil()
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

    os = OpenstackUtil()

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





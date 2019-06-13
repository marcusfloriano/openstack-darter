
import openstack.cloud

from darter.models import Domain, Project

'''This class is for calculate the measurement for items into openstack '''


class Openstack:

    def __init__(self, cloud):
        self.cloud = cloud
        self.conn = openstack.connect(cloud=self.cloud)

    def get_domains(self):
        domains = []
        for domain in self.conn.identity.domains():
            d = Domain(domain.id, domain.name, self.cloud)
            domains.append(d.to_json())
        return domains

    def get_projects(self, cloud, domain):
        conn = openstack.connect(cloud=cloud)
        projects = []
        for project in conn.identity.projects(domain_id=domain.id):
            projects.append(project)
        return projects

    def get_compute_totals(self, cloud, project):
        conn = openstack.openstack_cloud(cloud=cloud)
        quota = conn.get_compute_limits(name_or_id=project.id)
        return {
            "total_cores_used": quota.total_cores_used,
            "total_instances_used": quota.total_instances_used,
            "total_ram_used": quota.total_ram_used,
            "max_total_cores": quota.max_total_cores,
            "max_total_instances": quota.max_total_instances,
            "max_total_ram_size": quota.max_total_ram_size
        }


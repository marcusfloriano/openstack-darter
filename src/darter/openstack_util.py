
import openstack.cloud

from darter.models import Domain, Project

'''This class is for calculate the measurement for items into openstack '''


class OpenstackUtil:

    def __init__(self, region):
        self.region = region
        self.conn = openstack.connect(cloud=self.region)
        self.conn_cloud = openstack.openstack_cloud(cloud=self.region)

    def get_domains(self):
        domains = []
        for domain in self.conn.identity.domains():
            d = Domain(domain.id, domain.name, self.region)
            domains.append(d.to_json())
        return domains

    def get_projects(self, domain_id):
        projects = []
        for project in self.conn.identity.projects(domain_id=domain_id):
            p = Project(project.id, project.name, domain_id)
            p = self.get_compute_totals(p)
            projects.append(p.to_json())
        return projects

    def get_compute_totals(self, project: Project):
        quota = self.conn_cloud.get_compute_limits(name_or_id=project.uuid)

        project.total_cores_used = quota.total_cores_used
        project.total_instances_used = quota.total_instances_used
        project.total_ram_used = quota.total_ram_used
        project.max_total_cores = quota.max_total_cores
        project.max_total_instances = quota.max_total_instances
        project.max_total_ram_size = quota.max_total_ram_size

        return project


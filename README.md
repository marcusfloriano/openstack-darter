# README

## Description

The tool is for monitoring the capacity from openstack, which monitoring total of quote and total used.

The metrics being measured are:

* total_domains - Total domains in openstack
* total_projects - Total projects in openstack
* total_cores_used - Total vCPUs used in openstack
* max_total_cores - Total vCPUs in quota for all projects in openstack
* total_instances_used - Total Instances used in openstack
* max_total_instances - Total Instances in quota for all projects in openstack
* total_ram_used - Total Memory use in openstack
* max_total_ram_size - Total Mempry in quita for all projects in opesntack


## Prerequisites

* Admin user/password of openstack
* Grafana for show the measured
* InfluxDB for store the measured
* Redis for processing jobs

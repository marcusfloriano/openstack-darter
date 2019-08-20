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
* Redis for processing jobs


## Development Environment

### Prerequisites

* https://github.com/eoranged/rq-dashboard
* Docker and Docker Compose


### Start

docker-compose up -d
rq worker -c settings -v
rq-dashboard


## Commands for get infos with openstack-cli

openstack volume list --long --all -f value -c Type -c Size | grep Standard-Performance | sort | awk '{std+=$1;} END {print "STD="std}'
openstack volume list --long --all -f value -c Type -c Size | grep High-Performance |  sort |  awk '{gen1+=$1;} END {print "high-G1="gen1}'
openstack volume list --long --all -f value -c Type -c Size | grep High-Performance-Gen2 |  sort |  awk '{gen2+=$1;} END {print "high-G2="gen2}'
openstack server list --all-project --format csv | awk '/\".*\-.*\-.*\-.*\-.*?\"/ {split($0,arr,","); print arr[1]}' | wc -l | awk '{print "servers="$1}'
openstack hypervisor list --long | grep "comp-1" | awk '{print $16}' | sort | awk '{memo+=($1-16384);} END {print "memoria="memo}'
openstack hypervisor list --long | grep "comp-2" | awk '{print $16}' | sort | awk '{memo+=($1-32768);} END {print "memoria="memo}'
openstack hypervisor list --long | grep "comp" | awk '{print $12}' | sort | awk '{cpu+=$1;} END {print "vcpu="cpu}'





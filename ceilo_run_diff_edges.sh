#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

source devstack/openrc rajsimman demo1 EDGE-YK-1 iam.savitestbed.ca
OS_PASSWORD=jNXoc2Wd

python ceilo_run_commands.py

source devstack/openrc rajsimman demo1 CORE iam.savitestbed.ca
OS_PASSWORD=jNXoc2Wd

python ceilo_run_commands.py

#source devstack/openrc rajsimman demo1 EDGE-CT-1 iam.savitestbed.ca
#OS_PASSWORD=jNXoc2Wd

#python ceilo_run_commands.py

source devstack/openrc rajsimman demo1 EDGE-WT-1 iam.savitestbed.ca
OS_PASSWORD=jNXoc2Wd

python ceilo_run_commands.py

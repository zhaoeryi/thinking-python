#!/bin/bash

# Preparation
sudo rm devstack -rf
git clone https://github.com/openstack-dev/devstack.git
cd devstack

# Basic Setup
echo ADMIN_PASSWORD=passw0rd > localrc
echo HOST_IP=127.0.0.1 >> localrc
echo SERVICE_HOST=127.0.0.1 >> localrc
echo MYSQL_PASSWORD=passw0rd >> localrc
echo RABBIT_PASSWORD=passw0rd >> localrc
echo SERVICE_PASSWORD=passw0rd >> localrc
echo SERVICE_TOKEN=tokentoken >> localrc

# Enable Neutron
echo Q_PLUGIN=openvswitch >> localrc

echo disable_service n-net >> localrc
echo enable_service q-svc >> localrc
echo enable_service q-agt >> localrc
echo enable_service q-dhcp >> localrc
echo enable_service q-l3 >> localrc
echo enable_service q-meta >> localrc
echo enable_service neutron >> localrc
# Optional, to enable tempest configuration as part of devstack
echo enable_service tempest >> localrc

./stack.sh

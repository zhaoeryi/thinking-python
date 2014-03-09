#!/usr/bin/python

import sys
from neutron.plugins.openvswitch.agent.ovs_neutron_agent import main

if __name__ == "__main__":
    sys.argv = ['/usr/local/bin/neutron-openvswitch-agent', '--config-file', '/etc/neutron/neutron.conf', '--config-file', '/etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini']
    main()


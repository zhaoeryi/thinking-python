#!/usr/bin/python

import sys
from neutron import server

def start_neutron_server():
    # ML2 Plugin
    # sys.argv = ['/usr/local/bin/neutron-server', '--config-file', '/etc/neutron/neutron.conf', '--config-file', '/etc/neutron/plugins/ml2/ml2_conf.ini']
    
    # OVS Plugin
    sys.argv = ['/usr/local/bin/neutron-server', '--config-file', '/etc/neutron/neutron.conf', '--config-file', '/etc/neutron/plugins/openvswitch/ovs_neutron_plugin.ini']
    server.main()
    
        
if __name__ == "__main__":
    start_neutron_server()


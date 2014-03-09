#!/usr/bin/python

import sys
from neutron.agent.dhcp_agent import main

if __name__ == "__main__":
    sys.argv = ['/usr/local/bin/neutron-dhcp-agent', '--config-file', '/etc/neutron/neutron.conf', '--config-file', '/etc/neutron/dhcp_agent.ini']
    main()


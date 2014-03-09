#!/usr/bin/python

import sys
from neutron.agent.l3_agent import main

if __name__ == "__main__":
    sys.argv = ['/usr/local/bin/neutron-l3-agent', '--config-file', '/etc/neutron/neutron.conf', '--config-file', '/etc/neutron/l3_agent.ini']
    main()


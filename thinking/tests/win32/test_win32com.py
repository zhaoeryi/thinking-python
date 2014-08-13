from __future__ import print_function

import sys

from thinking.tests import base


def get_windows_network_adapters():
    # http://msdn.microsoft.com/en-us/library/windows/desktop/aa393259%28v=vs.85%29.aspx
    """Get the list of windows network adapters."""
    import win32com.client
    wbem_locator = win32com.client.Dispatch('WbemScripting.SWbemLocator')
    wbem_service = wbem_locator.ConnectServer('.', 'root\cimv2')
    wbem_network_adapters = wbem_service.InstancesOf('Win32_NetworkAdapter')
    network_adapters = []
    for adapter in wbem_network_adapters:
        if (adapter.NetConnectionStatus == 2 or
            adapter.NetConnectionStatus == 7):
            adapter_name = adapter.NetConnectionID
            mac_address = adapter.MacAddress.lower()
            config = adapter.associators_(
                          'Win32_NetworkAdapterSetting',
                          'Win32_NetworkAdapterConfiguration')[0]
            ip_address = ''
            subnet_mask = ''
            if config.IPEnabled:
                ip_address = config.IPAddress[0]
                subnet_mask = config.IPSubnet[0]
                # config.DefaultIPGateway[0]
            network_adapters.append({'name': adapter_name,
                                    'mac-address': mac_address,
                                    'ip-address': ip_address,
                                    'subnet-mask': subnet_mask})
    return network_adapters


class Win32comTestCase(base.ThinkingTestCase):
    def test_platform(self):

    def test_get_windows_network_adapters(self):
        if sys.platform == 'win32':
            adapters = get_windows_network_adapters()

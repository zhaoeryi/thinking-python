from __future__ import print_function

import sys

from thinking.tests import base


if sys.platform == 'win32':
    import wmi


class WMIcomTestCase(base.ThinkingTestCase):

    def setUp(self):
        if sys.platform == 'win32':
            self._conn_cimv2 = wmi.WMI(moniker='//./root/cimv2')
        super(WMIcomTestCase, self).setUp()

    def _get_cpus_info(self):
        cpus = self._conn_cimv2.query("SELECT * FROM Win32_Processor "
                                      "WHERE ProcessorType = 3")
        cpus_list = []
        for cpu in cpus:
            cpu_info = {'Architecture': cpu.Architecture,
                        'Name': cpu.Name,
                        'Manufacturer': cpu.Manufacturer,
                        'NumberOfCores': cpu.NumberOfCores,
                        'NumberOfLogicalProcessors':
                        cpu.NumberOfLogicalProcessors}
            cpus_list.append(cpu_info)
        return cpus_list

    def test_get_cpus_info(self):
        cpus_list = self._get_cpus_info()

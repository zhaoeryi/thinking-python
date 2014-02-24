import _hacking
import sys

if sys.platform == 'win32':
    import wmi
    
class WMIcomTestCase(_hacking.HackingTestCase):
    
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
        for cpu_info in cpus_list:
            print cpu_info
        
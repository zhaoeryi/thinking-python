import testtools
import logging.config
import sys
from oslo.config import cfg

print "package ", __file__, "is loaded"

# see example at: nova\openstack\common\log.py
log_config = "C:\Z\workspace\stack\_hacking\_hacking\logging.conf"
if log_config:
    logging.config.fileConfig(log_config)

logger = logging.getLogger("hacking")

CONF = cfg.CONF
CONF(args=['--config-file', 'C:\\Z\\workspace\\stack\\_hacking\\_hacking\\ _hacking.conf'])

class HackingTestCase(testtools.TestCase):

    def setUp(self):
        print "\n"
        # print "====================", self.id(), "===================="
        print "==============================", self._testMethodName, "=============================="
        """Run before each test method to initialize test environment."""
        super(HackingTestCase, self).setUp()

    def tearDown(self):
        super(HackingTestCase, self).tearDown()

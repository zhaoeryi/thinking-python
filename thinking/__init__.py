import testtools
import logging.config
import sys
from oslo.config import cfg

print "package ", __file__, "is loaded"

# see example at: nova\openstack\common\log.py
log_config = "/home/zhyizhyi/workspace/stack/thinking-python/thinking/logging.conf"
if log_config:
    logging.config.fileConfig(log_config)

logger = logging.getLogger("thinking")

CONF = cfg.CONF
CONF(args=['--config-file', '/home/zhyizhyi/workspace/stack/thinking-python/thinking/thinking.conf'])

class ThinkingTestCase(testtools.TestCase):

    def setUp(self):
        print "\n"
        # print "====================", self.id(), "===================="
        print "==============================", self._testMethodName, "=============================="
        """Run before each test method to initialize test environment."""
        super(ThinkingTestCase, self).setUp()

    def tearDown(self):
        super(ThinkingTestCase, self).tearDown()

import testtools

class ThinkingTestCase(testtools.TestCase):

    def setUp(self):
        print "\n"
        # print "====================", self.id(), "===================="
        print "==============================", self._testMethodName, "=============================="
        """Run before each test method to initialize test environment."""
        super(ThinkingTestCase, self).setUp()

    def tearDown(self):
        super(ThinkingTestCase, self).tearDown()
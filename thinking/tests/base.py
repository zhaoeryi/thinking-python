from __future__ import print_function

import testtools


class ThinkingTestCase(testtools.TestCase):

    def setUp(self):
        """Run before each test method to initialize test environment."""
        super(ThinkingTestCase, self).setUp()

    def tearDown(self):
        super(ThinkingTestCase, self).tearDown()

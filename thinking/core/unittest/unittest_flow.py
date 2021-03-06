from __future__ import print_function
import unittest

def setUpModule():
    print("setUpModule")
 
def tearDownModule():
    print("tearDownModule")
    
class MyTestCase(unittest.TestCase):

    def my_fixture_setup(self):
        print("++++ my_fixture_setup")
        
    def my_fixture_cleanup(self):
        print("++++ my_fixture_cleanup")
        print()
           
    def setUp(self):
        super(MyTestCase, self).setUp()
        self.my_fixture_setup()
        self.addCleanup(self.my_fixture_cleanup)

    def tearDown(self):
        super(MyTestCase, self).tearDown()
        print("++++ tearDown")
        
    def test_case_1(self):
        print("++++ test case 1")

    def test_case_2(self):
        print("++++ test case 2")
          
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        print()

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
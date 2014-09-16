from __future__ import print_function
import fixtures
import testtools

class MyFixture(fixtures.Fixture):
    def setUp(self):
        super(MyFixture,self).setUp()
        self.frobnozzle = 42
        print("++++ MyFixture.setup()")
        
    def cleanUp(self):
        super(MyFixture,self).cleanUp()
        print("++++ MyFixture.cleanup()")
        print()
           
class MyTestCase(testtools.TestCase):
           
    def setUp(self):
        super(MyTestCase, self).setUp()
        self.my_fixture = self.useFixture(MyFixture())
        print("++++ setUp")

    def tearDown(self):
        super(MyTestCase, self).tearDown()
        print("++++ tearDown")
        
    def test_case_1(self):
        self.assertEqual(42, self.my_fixture.frobnozzle)
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
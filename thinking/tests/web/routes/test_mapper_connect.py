from __future__ import print_function
from thinking.tests import base
import webob
from thinking.web.dummy_controller import DummyController
from routes import Mapper


class MapperConnectTestCase(base.ThinkingTestCase):

    def test_dummy_controller(self):
        controller = DummyController()
        value = controller.method_not_exits("aaabbbccc")
        self.assertEqual("method_not_exits()", value)

    def test_mapper_basic(self):
        routename = "test_mapper_basic"
        routepath = "/dummy"

        map = Mapper()
        map.connect(routename, routepath,
                        controller=DummyController(),
                        key1="value1", key2="value2")

        # test invalid url
        for invalid_url in ("/", "dummy", "/dummy/123", "dummy123"):
            match_dict = map.match(invalid_url)
            self.assertIsNone(match_dict)

        # test valid url
        match_dict = map.match("/dummy")
        self.assertIsNotNone(match_dict)
        self.assertEquals(match_dict["key1"], "value1")
        self.assertEquals(match_dict["key2"], "value2")
        self.assertIsInstance(match_dict["controller"], unicode)

    def test_mapper_with_placeholder(self):
        routename = "test_mapper_with_placeholder"
        routepath = "/dummy/{father_var}/{son_var}/{id_var}.html"

        map = Mapper()
        map.connect(routename, routepath,
                        controller=DummyController(),
                        key1="value1", key2="value2")

        #
        match_dict = map.match("/dummy/father123/son456/789.html")
        self.assertIsNotNone(match_dict)
        self.assertEquals(match_dict["father_var"], "father123")
        self.assertEquals(match_dict["son_var"], "son456")
        self.assertEquals(match_dict["id_var"], "789")

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
        route_name = self._testMethodName
        route_path = "/dummy"

        map = Mapper()
        map.connect(route_name, route_path,
                        controller=DummyController(),
                        key1="value1", key2="value2")

        # test invalid url
        for invalid_url in ("/", "dummy", "/dummy/", "/dummy/123", "dummy123"):
            match_dict = map.match(invalid_url)
            self.assertIsNone(match_dict)

        # test valid url
        match_dict = map.match("/dummy")
        self.assertIsInstance(match_dict, dict)
        self.assertEquals(match_dict["key1"], "value1")
        self.assertEquals(match_dict["key2"], "value2")
        self.assertIsInstance(match_dict["controller"], unicode)

    def test_mapper_with_placeholder(self):
        route_name = self._testMethodName
        route_path = "/dummy/{father_var}/{son_var}/{id_var}.html"

        map = Mapper()
        map.connect(route_name, route_path,
                        controller=DummyController(),
                        key1="value1", key2="value2")

        #
        match_dict = map.match("/dummy/father123/son456/789.html")
        self.assertIsInstance(match_dict, dict)
        self.assertEquals(match_dict["father_var"], "father123")
        self.assertEquals(match_dict["son_var"], "son456")
        self.assertEquals(match_dict["id_var"], "789")

    def test_mapper_with_regex(self):
        route_name = self._testMethodName
        route_path = "/dummy/{year}/{month}"

        map = Mapper()
        map.connect(route_name, route_path, controller=DummyController(),
          action="view", year=2004,
          requirements=dict(year=R"\d{2013,2014}", month=R"\d{10,11}"))

        # test valid url
        for invalid_url in ("/dummy/2013/10", "/dummy/2013/11", "/dummy/2014/10", "/dummy/2014/11"):
            match_dict = map.match(invalid_url)
            self.assertIsNone(match_dict)

        # test invalid url
        for invalid_url in ("/dummy/2013/9", "/dummy/2015/10"):
            match_dict = map.match(invalid_url)
            self.assertIsNone(match_dict)

    def test_mapper_with_conditions(self):
        route_name = self._testMethodName
        route_path = "/dummy/fathers/"

        map = Mapper()
        map.connect(route_name, route_path,
                        controller=DummyController(),
                        key1="value1", key2="value2", conditions=dict(method=["GET", "HEAD"]))

        #
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = map.match("/dummy/fathers/", environ)
        self.assertIsInstance(match_dict, dict)
        
        environ = {"REQUEST_METHOD":"HEAD"}
        match_dict = map.match("/dummy/fathers/", environ)
        self.assertIsInstance(match_dict, dict)
        
        environ = {"REQUEST_METHOD":"PUT"}
        match_dict = map.match("/dummy/fathers/", environ)
        self.assertIsNone(match_dict)

    def test_mapper_with_format(self):
        route_name = self._testMethodName
        route_path = "/dummy/fathers/{id_var}{.format}"

        map = Mapper()
        map.connect(route_name, route_path,
                        controller=DummyController(),
                        key1="value1", key2="value2")

        # Format is ".mp3"
        match_dict = map.match("/dummy/fathers/123.mp3")
        self.assertIsInstance(match_dict, dict)
        self.assertEquals(match_dict["id_var"], "123")
        self.assertEquals(match_dict["format"], "mp3")
        
        # Format is none
        match_dict = map.match("/dummy/fathers/456")
        self.assertIsInstance(match_dict, dict)
        print(match_dict)
        self.assertEquals(match_dict["id_var"], "456")
        self.assertIsNone(match_dict["format"])
        
        
        
        
from __future__ import print_function
from thinking.tests import base
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
        controller = DummyController()
        
        mapper = Mapper()
        mapper.connect(route_name, route_path,
                        controller=controller,
                        key1="value1", key2="value2")

        # test invalid url
        for invalid_url in ("/", "dummy", "/dummy/", "/dummy/123", "dummy123"):
            match_dict = mapper.match(invalid_url)
            self.assertIsNone(match_dict)

        # test valid url
        match_dict = mapper.match("/dummy")
        self.assertDictEqual(match_dict, {'key2': u'value2', 'controller': str(controller).decode('utf-8'), 'key1': u'value1'})

    def test_mapper_with_placeholder(self):
        route_name = self._testMethodName
        route_path = "/dummy/{father_var}/{son_var}/{id_var}.html"
        controller = DummyController()
        mapper = Mapper()
        mapper.connect(route_name, route_path,
                        controller=controller,
                        key1="value1", key2="value2")

        match_dict = mapper.match("/dummy/father123/son456/789.html")
        self.assertIsInstance(match_dict, dict)
        
        self.assertDictEqual(match_dict, {'father_var': u'father123', 'id_var': u'789', 'key2': u'value2', 'key1': u'value1', 'controller': str(controller).decode('utf-8'), 'son_var': u'son456'})
        

    def test_mapper_with_regex(self):
        route_name = self._testMethodName
        route_path = "/dummy/{year}/{month}"

        mapper = Mapper()
        mapper.connect(route_name, route_path, controller=DummyController(),
          action="view", year=2004,
          requirements=dict(year=R"\d{2013,2014}", month=R"\d{10,11}"))

        # test valid url
        for invalid_url in ("/dummy/2013/10", "/dummy/2013/11", "/dummy/2014/10", "/dummy/2014/11"):
            match_dict = mapper.match(invalid_url)
            self.assertIsNone(match_dict)

        # test invalid url
        for invalid_url in ("/dummy/2013/9", "/dummy/2015/10"):
            match_dict = mapper.match(invalid_url)
            self.assertIsNone(match_dict)

    def test_mapper_with_conditions(self):
        route_name = self._testMethodName
        route_path = "/dummy/fathers/"
        controller = DummyController()
        
        mapper = Mapper()
        mapper.connect(route_name, route_path,
                        controller=controller,
                        key1="value1", key2="value2", conditions=dict(method=["GET", "HEAD"]))

        #
        environ = {"REQUEST_METHOD":"GET"}
        match_dict = mapper.match("/dummy/fathers/", environ)
        self.assertDictEqual(match_dict, {'key2': u'value2', 'key1': u'value1', 'controller': str(controller).decode('utf-8')})
        
        environ = {"REQUEST_METHOD":"HEAD"}
        match_dict = mapper.match("/dummy/fathers/", environ)
        self.assertDictEqual(match_dict, {'key2': u'value2', 'key1': u'value1', 'controller': str(controller).decode('utf-8')})
        
        environ = {"REQUEST_METHOD":"PUT"}
        match_dict = mapper.match("/dummy/fathers/", environ)
        self.assertIsNone(match_dict)

    def test_mapper_with_format(self):
        route_name = self._testMethodName
        route_path = "/dummy/fathers/{id_var}{.format}"
        controller = DummyController()

        mapper = Mapper()
        mapper.connect(route_name, route_path,
                        controller=controller,
                        key1="value1", key2="value2")

        # Format is ".mp3"
        match_dict = mapper.match("/dummy/fathers/123.mp3")
        self.assertDictEqual(match_dict, {'key2': u'value2', 'controller': str(controller).decode('utf-8'), 'format': u'mp3', 'key1': u'value1', 'id_var': u'123'})
        # Format is none
        match_dict = mapper.match("/dummy/fathers/456")
        self.assertDictEqual(match_dict, {'key2': u'value2', 'controller': str(controller).decode('utf-8'), 'format': None, 'key1': u'value1', 'id_var': u'456'})
        
        
        
        

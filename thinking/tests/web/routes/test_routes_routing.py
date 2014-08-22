from __future__ import print_function
from thinking.tests import base
import webob
from thinking.web.dummy_controller import DummyController
from routes import Mapper
from routes.middleware import RoutesMiddleware
import routes
import httplib2
from paste import deploy
import os 

class MyController(object):
    def getlist(self, mykey):
        return "getlist(), mykey=" + mykey

class MyResource(object):

    def __init__(self, controller):
        self._controller = controller

    def __call__(self, environ, start_response):
        action_args = environ['wsgiorg.routing_args'][1].copy()
        try:
            del action_args['controller']
        except KeyError:
            pass

        try:
            del action_args['format']
        except KeyError:
            pass
        
        action = action_args.pop('action', None)
        controller_meth = getattr(self._controller, action)
        result = controller_meth(**action_args)
        
        start_response('200 OK', [('Content-Type', 'text/plain')])
        #return [result]
        return [1234]
        
class MyRouter(object):
    def __init__(self):
        # Build mapper
        route_name = "MyRouter"
        route_path = "/dummies"
        
        my_controller = MyController()
        my_resource = MyResource(my_controller) 
        
        mapper = Mapper()
        mapper.connect(route_name, route_path,
                        controller=my_resource,
                        action="getlist",
                        mykey="myvalue",
                        conditions={"method": ['GET']})
        self._router = routes.middleware.RoutesMiddleware(self._dispatch, mapper)

    @classmethod
    def factory(cls, global_config, **local_config):
        return cls()
    
    def __call__(self, environ, start_response):
        """Route the incoming request to a controller based on self.map.

        If no match, return a 404.

        """
        return self._router

    @staticmethod
    def _dispatch(environ, start_response):
        """Dispatch the request to the appropriate controller.

        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.

        """
        match_dict = environ['wsgiorg.routing_args'][1]
        if not match_dict:
            return webob.exc.HTTPNotFound()
        app = match_dict['controller']
        return app
              
class MiddleWareTestCase(base.ThinkingTestCase):
    
    def _loadapp(self):
        config_path = os.path.join(os.path.dirname(__file__), 'test_routes_routing.ini')
        composite_name = "test_wsgi_comp"
        wsgi_site = deploy.loadapp("config:%s" % os.path.abspath(config_path), composite_name)
        return wsgi_site

    def test_hello_world(self):
        wsgi_site = self._loadapp()
        resp = webob.Request.blank('/').get_response(wsgi_site)

        print("resp=%s" % (resp))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, "app1,filter2,filter1")
        
    def test_middleware_routing(self):

        # Build router
        router = MyRouter()
        
        # send request
        resp = webob.Request.blank('/dummies').get_response(router)
        self.assertEqual(resp.status_code, 200)

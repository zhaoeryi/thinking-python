from __future__ import print_function
from thinking.tests import base
import webob
from thinking.web.dummy_controller import DummyController
from routes import Mapper
from routes.middleware import RoutesMiddleware
import routes
import httplib2
from thinking.web import wsgi_server

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
        return (result)
        
        
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
    
    def test_middleware_routing(self):

        # Build router
        router = MyRouter()
        
        import eventlet
        eventlet.monkey_patch(os=False)

        server = wsgi_server.WsgiServer("test_hello_world", app=MyRouter(),
                                  host="127.0.0.1", port=8080)
        server.start()
        client = httplib2.Http()
        resp, body = client.request(
            "http://127.0.0.1:8080/dummies", "get", headers=None, body=None)
        print("resp=%s, body=%s" % (resp, body))

        self.assertEqual(resp.status, 200)
        self.assertEqual(body, "hello world!")

        server.stop()
        
        # send request
        self.assertEqual(resp.body, "getlist(), mykey=myvalue")

from __future__ import print_function
from thinking.tests import base
from routes import Mapper
import webob.exc
import routes.middleware

class MyController(object):
    def getlist(self, mykey):
        print("step 4: MyController's getlist(self, mykey) is invoked")
        return "getlist(), mykey=" + mykey

class MyApplication(object):
    """Test application to call from router."""

    def __init__(self, controller):
        self._controller = controller
        
    def __call__(self, environ, start_response):
        print("step 3: MyApplication is invoked")
        
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
        controller_method = getattr(self._controller, action)
        result = controller_method(**action_args)
        
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [result]

class MyRouter(object):
    """Test router."""

    def __init__(self):
        route_name = "dummy_route"
        route_path = "/dummies"
        
        my_application = MyApplication(MyController()) 
        
        self.mapper = Mapper()
        self.mapper.connect(route_name, route_path,
                        controller=my_application,
                        action="getlist",
                        mykey="myvalue",
                        conditions={"method": ['GET']})
        
        
        self._router = routes.middleware.RoutesMiddleware(self._dispatch,
                                                          self.mapper)

    def __call__(self, environ, start_response):
        """Route the incoming request to a controller based on self.map.

        If no match, return a 404.

        """
        print("step 1: MyRouter is invoked")
        return self._router(environ, start_response)

    @staticmethod
    def _dispatch(environ, start_response):
        """Dispatch the request to the appropriate controller.

        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.

        """
        print("step 2: RoutesMiddleware is invoked, calling our _dispatch back")
        
        match_dict = environ['wsgiorg.routing_args'][1]
        if not match_dict:
            return webob.exc.HTTPNotFound()
        app = match_dict['controller']
        return app(environ, start_response)
        
class RoutingTestCase(base.ThinkingTestCase):

    def test_router(self):
        router = MyRouter()
        result = webob.Request.blank('/dummies').get_response(router)
        self.assertEqual(result.body, "getlist(), mykey=myvalue")


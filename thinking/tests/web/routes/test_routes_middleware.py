from __future__ import print_function
from thinking.tests import base
import webob
from thinking.web.dummy_controller import DummyController
from routes import Mapper
from routes.middleware import RoutesMiddleware
import routes

class MiddleWareTestCase(base.ThinkingTestCase):
    
    def test_middleware_match_ok(self):
        controller = DummyController()
        
        def wsgi_app(environ, start_response):
            '''
             middleware will sets the following WSGI variables if url match
            '''
            url, match_dict = environ['wsgiorg.routing_args']
            routes_route = environ['routes.route']   
            routes_url = environ['routes.url']  
             
            self.assertDictEqual(match_dict, {'controller': str(controller).decode('utf-8'), 'mykey': u'myvalue'})
            self.assertIsInstance(routes_route, routes.route.Route)
            self.assertIsInstance(routes_url, routes.util.URLGenerator)
            self.assertTrue(url == routes_url) 
            
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return ['hello world!']
        
        # Build mapper
        route_name = self._testMethodName
        route_path = "/dummy"
        
        mapper = Mapper()
        mapper.connect(route_name, route_path,
                        controller=controller,
                        mykey="myvalue")
        
        # Build router
        router = routes.middleware.RoutesMiddleware(wsgi_app, mapper)
        
        # send request
        resp = webob.Request.blank('/dummy').get_response(router)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, "hello world!")

    def test_middleware_match_fail(self):
        controller = DummyController()
        
        def wsgi_app(environ, start_response):
            url, match_dict = environ['wsgiorg.routing_args']
            routes_route = environ['routes.route']   
            routes_url = environ['routes.url']  
             
            self.assertDictEqual(match_dict, {})
            self.assertIsNone(routes_route)
            self.assertIsInstance(routes_url, routes.util.URLGenerator)
            self.assertTrue(url == routes_url) 
            
            start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
            return ['not found!']
        
        # Build mapper
        route_name = self._testMethodName
        route_path = "/dummy"
        
        mapper = Mapper()
        mapper.connect(route_name, route_path,
                        controller=controller,
                        mykey="myvalue")
        
        # Build router
        router = routes.middleware.RoutesMiddleware(wsgi_app, mapper)
        
        # send request
        resp = webob.Request.blank('/dummy/impossible_to_match').get_response(router)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.body, "not found!")


    def test_middleware_routing(self):
        
        class DemoController(object):
            def getlist(self, mykey):
                return "getlist(), mykey=" + mykey
    
        controller_app = DemoController()
        
        def router_app(environ, start_response):
            '''
             middleware will sets the following WSGI variables if url match
            '''
            url, match_dict = environ['wsgiorg.routing_args']
            
            if not match_dict:
                return webob.exc.HTTPNotFound()
            
            action_args = match_dict.copy()
            try:
                del action_args['controller']
            except KeyError:
                pass

            try:
                del action_args['format']
            except KeyError:
                pass
            
            action = action_args.pop('action', None)
            controller_meth = getattr(controller_app, action)
            result = controller_meth(**action_args)
            
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [result]
        
        # Build mapper
        route_name = self._testMethodName
        route_path = "/dummies"
        
        mapper = Mapper()
        mapper.connect(route_name, route_path,
                        controller=controller_app,
                        action="getlist",
                        mykey="myvalue",
                        conditions={"method": ['GET']})

        # Build router
        router = routes.middleware.RoutesMiddleware(router_app, mapper)
        
        # send request
        resp = webob.Request.blank('/dummies').get_response(router)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, "getlist(), mykey=myvalue")

from __future__ import print_function
import os
from paste import deploy
import routes.middleware
from thinking.tests import base
import webob.dec
import webob.exc
from wsgiref import simple_server

import thinking


logger = thinking.logger


# app
class action_contr():
    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Hello World!']


# app
class api_router():

    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        _mapper = routes.Mapper()

        # match http://127.0.0.1:8080/hacking/test?a=b
        _mapper.connect("/test", controller=action_contr())
        _router = routes.middleware.RoutesMiddleware(self._dispatch, _mapper)

        response = _router(environ, start_response)
        return response

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls()

    # _dispatch will return WSGI application, webob.dec.wsgify will invoke it, also return the decorate the response.
    @staticmethod
    @webob.dec.wsgify(RequestClass=webob.Request)
    def _dispatch(req):
        """Dispatch the request to the appropriate controller.

        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.

        """
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller']
        return app


def start_server():
    logger.debug("start server......")
    configfile = "thinking/routes/app_routes.ini"
    compositename = "test_comp"
    wsgi_app = deploy.loadapp("config:%s" % os.path.abspath(configfile), compositename)
    server = simple_server.make_server('localhost', 8080, wsgi_app)
    server.serve_forever()


class RoutesTestCase(base.ThinkingTestCase):
    def test_api_router(self):
        result = webob.Request.blank('/test').get_response(api_router())
        self.assertEqual(result.body, "Hello World!")

if __name__ == '__main__':
    start_server()
    pass

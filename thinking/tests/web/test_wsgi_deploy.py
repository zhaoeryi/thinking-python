from __future__ import print_function
import httplib2
import webob
from thinking.tests import base
from thinking.web import wsgi_server
import os
from paste import deploy
# from wsgiref import simple_server


# Filter
class test_wsgi_filter1():
    def __init__(self, app):
        self.app = app
        pass

    def __call__(self, environ, start_response):
        ret = self.app(environ, start_response)
        ret = ret + [",filter1"]
        return ret

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls


# Filter
class test_wsgi_filter2():

    def __init__(self, app):
        self.app = app
        pass

    def __call__(self, environ, start_response):
        ret = self.app(environ, start_response)
        ret = ret + [",filter2"]
        return ret

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls


# app
class test_wsgi_app1():

    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        start_response("200 OK", [("Content-type", "text/plain")])
        return ["app1", ]

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls()


# app
class test_wsgi_app2():

    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        start_response("200 OK", [("Content-type", "text/plain")])
        return ["app2", ]

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls()


class WsgiDeployTestCase(base.ThinkingTestCase):

    def _loadapp(self):
        config_path = "test_wsgi_deploy.ini"
        composite_name = "test_wsgi_comp"
        wsgi_site = deploy.loadapp("config:%s" % os.path.abspath(config_path), composite_name)
        return wsgi_site

    def test_hello_world(self):
        wsgi_site = self._loadapp()
        resp = webob.Request.blank('/').get_response(wsgi_site)

        print("resp=%s" % (resp))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, "app1,filter2,filter1")

    def test_hello_world_with_server(self):
        import eventlet
        eventlet.monkey_patch(os=False)

        wsgi_site = self._loadapp()
        server = wsgi_server.WsgiServer("test_hello_world", app=wsgi_site,
                                  host="127.0.0.1", port=8080)
        server.start()
        client = httplib2.Http()
        resp, body = client.request(
            "http://127.0.0.1:8080", "get", headers=None, body=None)
        print("resp=%s, body=%s" % (resp, body))

        self.assertEqual(resp.status, 200)
        self.assertEqual(body, "app1,filter2,filter1")
        server.stop()


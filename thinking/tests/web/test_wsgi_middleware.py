import httplib2
import webob
from thinking.tests import base
from thinking.web import wsgi_server


def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ["hello world"]


class middleware(object):

    def __init__(self, app, encoding='utf8'):
        self.app = app

    def __call__(self, environ, start_response):
        content = self.app(environ, start_response)
        content.append(" with middleware")
        return content


class WsgiMiddleWareTestCase(base.ThinkingTestCase):

    def test_wsgi_middleware(self):
        # We warp the original WSGI application with middleware
        site = middleware(app)
        resp = webob.Request.blank('/').get_response(site)

        print("resp=%s" % (resp))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, "hello world with middleware")

    def test_wsgi_middleware_with_server(self):
        import eventlet
        eventlet.monkey_patch(os=False)

        site = middleware(app)
        server = wsgi_server.WsgiServer("test_hello_world", app=site,
                                  host="127.0.0.1", port=8080)
        server.start()
        client = httplib2.Http()
        resp, body = client.request(
            "http://127.0.0.1:8080", "get", headers=None, body=None)
        print("resp=%s, body=%s" % (resp, body))

        self.assertEqual(resp.status, 200)
        self.assertEqual(body, "hello world with middleware")

        server.stop()
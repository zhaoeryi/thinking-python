from __future__ import print_function
import httplib2
import webob
import webtest
from thinking.tests import base
from thinking.web import wsgi_server


def hello_world(env, start_response):
    if env['PATH_INFO'] != '/':
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return ['Not Found\r\n']

    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['hello world!']


class WsgiAppTestCase(base.ThinkingTestCase):

    def test_hello_world_with_webob(self):
        resp = webob.Request.blank('/').get_response(hello_world)

        print("resp=%s" % (resp))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, "hello world!")

    def test_hello_world_with_webtest(self):
        app = webtest.TestApp(hello_world)
        resp = app.get('/')
        print("resp=%s" % (resp))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, "hello world!")
        
    def test_hello_world_with_server(self):
        import eventlet
        eventlet.monkey_patch(os=False)

        server = wsgi_server.WsgiServer("test_hello_world", app=hello_world,
                                  host="127.0.0.1", port=8080)
        server.start()
        client = httplib2.Http()
        resp, body = client.request(
            "http://127.0.0.1:8080", "get", headers=None, body=None)
        print("resp=%s, body=%s" % (resp, body))

        self.assertEqual(resp.status, 200)
        self.assertEqual(body, "hello world!")

        server.stop()

    def test_hello_world_with_server111(self):
        import eventlet
        eventlet.monkey_patch(os=False)

        socket = eventlet.listen("127.0.0.1","8080")
        wsgi_kwargs = {
            'func': eventlet.wsgi.server,
            'sock': socket,
            'site': hello_world,
            'protocol': eventlet.wsgi.HttpProtocol,
            'debug': False
            }

        server = eventlet.spawn(**wsgi_kwargs)
        
        client = httplib2.Http()
        resp, body = client.request(
            "http://127.0.0.1:8080", "get", headers=None, body=None)
        print("resp=%s, body=%s" % (resp, body))

        self.assertEqual(resp.status, 200)
        self.assertEqual(body, "hello world!")
        
        server.kill()

        


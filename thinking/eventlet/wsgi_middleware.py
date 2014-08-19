import eventlet
from eventlet import wsgi


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

# We warp the original WSGI application with middleware
site = middleware(app)

# http://127.0.0.1:8080
wsgi.server(eventlet.listen(('', 8080)), site)

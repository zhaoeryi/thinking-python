import eventlet
from eventlet import wsgi


def my_app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ["hello myapp"]


class my_middleware(object):

    def __init__(self, app, encoding='utf8'):
        self.app = app

    def __call__(self, environ, start_response):
        content = self.app(environ, start_response)
        content.append(" with middleware")
        return content

# We warp the original WSGI application with middleware
my_site = my_middleware(my_app)

# http://127.0.0.1:8080
wsgi.server(eventlet.listen(('', 8080)), my_site)

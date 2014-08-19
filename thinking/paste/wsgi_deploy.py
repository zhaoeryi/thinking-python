from __future__ import print_function

import eventlet
from eventlet import wsgi as eventlet_wsgi
import os
from paste import deploy
from wsgiref import simple_server


# Filter
class wsgi_filter1():
    def __init__(self, app):
        self.app = app
        pass

    def __call__(self, environ, start_response):
        ret = self.app(environ, start_response)
        ret = ret + [", filter1"]
        return ret

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls


# Filter
class wsgi_filter2():

    def __init__(self, app):
        self.app = app
        pass

    def __call__(self, environ, start_response):
        ret = self.app(environ, start_response)
        ret = ret + [", filter2"]
        return ret

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls


# app
class wsgi_app1():

    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        start_response("200 OK", [("Content-type", "text/plain")])
        return ["wsgi app1", ]

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls()


# app
class wsgi_app2():

    def __init__(self):
        pass

    def __call__(self, environ, start_response):
        start_response("200 OK", [("Content-type", "text/plain")])
        return ["wsgi app2", ]

    @classmethod
    def factory(cls, global_conf, **kwargs):
        return cls()

if __name__ == '__main__':
    config_path = "wsgi_deploy.ini"
    composite_name = "wsgi_comp"
    wsgi_app = deploy.loadapp("config:%s" % os.path.abspath(config_path), composite_name)
    # server = simple_server.make_server('localhost', 8080, wsgi_app)
    # server.serve_forever()
    server = eventlet_wsgi.server(eventlet.listen(('', 8080)), wsgi_app)

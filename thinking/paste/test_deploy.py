from paste.deploy import loadapp
from webob import Request, Response
from wsgiref.simple_server import make_server
import os
import webob

# Filter
class test_filter1():
    def __init__(self, app):
        self.app = app
        pass
    def __call__(self, environ, start_response):
        print "test filter1 pre is called."
        ret = self.app(environ, start_response)
        print "test filter1 post is called."
        return ret
    @classmethod
    def factory(cls, global_conf, **kwargs):
        print "in test_filter1.factory", global_conf, kwargs
        return cls
  
# Filter
class test_filter2():
    def __init__(self, app):
        self.app = app
        pass
    def __call__(self, environ, start_response):
        print "test filter2 pre is called."
        ret = self.app(environ, start_response)
        print "test filter2 post is called."
        return ret
    @classmethod
    def factory(cls, global_conf, **kwargs):
        print "in test_filter2.factory", global_conf, kwargs
        return cls
      
# app
class test_app1():
    def __init__(self):
        pass
    def __call__(self, environ, start_response):
        print "test app1 is called."
        start_response("200 OK", [("Content-type", "text/plain")])
        return ["test app 1", ]
    @classmethod
    def factory(cls, global_conf, **kwargs):
        print "in test_app1.factory", global_conf, kwargs
        return cls()

# app
class test_app2():
    def __init__(self):
        pass
    def __call__(self, environ, start_response):
        print "test app2 is called."
        start_response("200 OK", [("Content-type", "text/plain")])
        return ["test app 2", ]
    @classmethod
    def factory(cls, global_conf, **kwargs):
        print "in test_app2.factory", global_conf, kwargs
        return cls()
    
if __name__ == '__main__':
    configfile = "test_deploy.ini"
    compositename = "test_comp"
    wsgi_app = loadapp("config:%s" % os.path.abspath(configfile), compositename)
    server = make_server('localhost', 8080, wsgi_app)
    server.serve_forever()
    pass

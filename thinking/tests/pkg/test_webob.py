import webob.dec
import webob.exc

from thinking.tests import base


class MyRequest(webob.Request):
    @property
    def is_local(self):
        return self.remote_addr == '127.0.0.1'


@webob.dec.wsgify(RequestClass=MyRequest)
def my_func(req):
    if req.is_local:
        return webob.response.Response('hi!')
    else:
        raise webob.exc.HTTPForbidden


class WsgifyTestCase(base.ThinkingTestCase):
    def test_fake(self):
        pass

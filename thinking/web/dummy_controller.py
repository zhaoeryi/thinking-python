from __future__ import print_function


class DummyMethod(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        print("method '%s' is invokded, args=%s, kwargs=%s" % (self.name, args, kwargs))
        return self.name + "()"


class DummyController(object):
    def _noop(self, *args, **kwargs):
        pass

    def __getattr__(self, key):
        return DummyMethod(key)

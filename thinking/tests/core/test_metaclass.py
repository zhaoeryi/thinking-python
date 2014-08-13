from __future__ import print_function
import six
from thinking.tests import base


# http://blog.jobbole.com/21351/
# see nova.api.openstack.wsgi.ControllerMetaclass
# see nova.tests.api.openstack.test_wsgi.ResourceTest:test_register_extensions
def mydecorator(*args, **kwargs):
    def decorator(f):
        f.wrapped = True
        return f

    if kwargs:
        return decorator
    else:
        return decorator(args[0])


class MyMeta(type):
    def __new__(meta, name, bases, cls_dct):
        # __new__ should be implemented when you want to control the creation of a new class
        return super(MyMeta, meta).__new__(meta, name, bases, cls_dct)

    def __init__(cls, name, bases, cls_dct):
        # __init__ should be implemented when you want to control the initialization of the new class after it has been created
        super(MyMeta, cls).__init__(name, bases, cls_dct)

    def __call__(cls, *args, **kwds):
        # __call__ is called when the already-created class is "called" to instantiate a new object.
        return type.__call__(cls, *args, **kwds)


@six.add_metaclass(MyMeta)
class MyKlass(object):

    barattr = 2


class MySubKlass(MyKlass):

    def __init__(self):
        super(MySubKlass, self).__init__()

    @mydecorator
    def foo(self):
        pass


class MetaClassTestCase(base.ThinkingTestCase):
    def test_new_instance(self):
        pass

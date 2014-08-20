from __future__ import print_function

# http://blog.jobbole.com/21351/
# see nova.api.openstack.wsgi.ControllerMetaclass
# see nova.tests.api.openstack.test_wsgi.ResourceTest:test_register_extensions

class MyMeta(type):
    def __new__(meta, name, bases, cls_dct):
        # __new__ should be implemented when you want to control the creation of a new class
        print('Inside MyMeta class __new__, [meta, name, bases, cls_dct]=', [meta, name, bases, cls_dct])
        return super(MyMeta, meta).__new__(meta, name, bases, cls_dct)

    def __init__(cls, name, bases, cls_dct):
        # __init__ should be implemented when you want to control the initialization of the new class after it has been created
        print('Inside MyMeta class __init__, [cls, name, bases, cls_dct]=', [cls, name, bases, cls_dct])
        super(MyMeta, cls).__init__(name, bases, cls_dct)

    def __call__(cls, *args, **kwds):
        # __call__ is called when the already-created class is "called" to instantiate a new object.
        print('Inside MyMeta class __call__, [cls, *args, **kwds]=', [cls, args, kwds])
        return type.__call__(cls, *args, **kwds)

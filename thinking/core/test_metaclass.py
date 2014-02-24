import _hacking

# http://blog.jobbole.com/21351/
# see nova.api.openstack.wsgi.ControllerMetaclass
# see nova.tests.api.openstack.test_wsgi.ResourceTest:test_register_extensions

def mydecorator(*args, **kwargs):
    def decorator(f):
        print "mydecorator: Inside mydecorator.wrap()"
        f.wrapped = True
        return f
    
    if kwargs:
        return decorator
    else:
        return decorator(args[0])
    
class MyMeta(type):
    def __new__(meta, name, bases, cls_dct):
        # __new__ should be implemented when you want to control the creation of a new class
        print "MyMeta.__new__: Allocating memory for class, name=", name, ", meta=" , meta, ", bases=", bases, ", cls_dct=", cls_dct
        return super(MyMeta, meta).__new__(meta, name, bases, cls_dct)
    
    def __init__(cls, name, bases, cls_dct):
        # __init__ should be implemented when you want to control the initialization of the new class after it has been created
        print "MyMeta.__init__: Initializing class, name=", name, ", bases=", bases, ", cls_dct=", cls_dct
        super(MyMeta, cls).__init__(name, bases, cls_dct)
        
        
        
    def __call__(cls, *args, **kwds):
        # __call__ is called when the already-created class is "called" to instantiate a new object.
        print 'MyMeta.__call__: cls=', str(cls), '*args=', str(args)
        return type.__call__(cls, *args, **kwds)


class MyKlass(object):
    __metaclass__ = MyMeta

    def __init__(self):
        print "MyKlass: Initializing instance"

    barattr = 2

class MySubKlass(MyKlass):
    
    def __init__(self):
        super(MySubKlass, self).__init__()
        print "MySubKlass: Initializing instance"

    @mydecorator
    def foo(self):
        pass
       
class MetaClassTestCase(_hacking.HackingTestCase):   
    def test_new_instance(self):
        pass

from __future__ import print_function
import six
from metaclass import MyMeta

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


@six.add_metaclass(MyMeta)
class MyClass(object):

    def __init__(self):
        print('Inside MyClass class __init__')

    bar_attr = 2

if __name__ == '__main__':
    print('\nStart to instantiate a new MyClass object')
    MyClass()

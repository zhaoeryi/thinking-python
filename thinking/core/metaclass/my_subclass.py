from __future__ import print_function
from my_class import MyClass


class MySubClass(MyClass):

    def __init__(self):
        print('Inside MySubKlass class __init__')
        super(MySubClass, self).__init__()

    def foo(self):
        pass

if __name__ == '__main__':
    print('\nStart to instantiate a new MySubClass object')
    MySubClass()

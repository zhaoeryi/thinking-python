# coding=utf-8
# http://blog.csdn.net/beckel/article/details/3945147
# function with decorator
'''
    @A(args)
    def f ():
        ......

    Python will convert the below into:

    def f():
        ......
    _deco = A(args)
    f = _deco(f)
'''

from __future__ import print_function

import logging

from thinking.tests import base


logger = logging.getLogger("hacking")

'''
The return value of the decorator function must be a function used to wrap the function to be decorated.
That is, Python will take the returned function and call it at decoration time, passing the function to be decorated.
That's why we have three levels of functions; the inner one is the actual replacement function.

decorator函数的返回值必须是一个封装待decorated函数的函数
也就是说，Python会保存返回函数然后在decoration期间调用，并传递待decorated函数
这也是为何有三层函数的原因：里面那个函数才是被替换的
'''


# 当参数为*arg时，表示接受一个元组；当参数为**arg时，表示接受一个字典
def decoratorFunctionWithArguments(*dec_args, **dec_kwargs):

    def wrap(f):
        print("Inside wrap()")

        def wrapped_f(*args):
            print("Inside wrapped_f()")
            print("Function  arguments:", args)
            print("Decorator arguments, dec_args=", dec_args, ", dec_kwargs=", dec_kwargs)
            f(*args)
            print("After f(*args)")
        return wrapped_f
    return wrap


class DecoratorClassWithoutArguments(object):
    def __init__(self, f):
        """
        If there are no decorator arguments, the function
        to be decorated is passed to the constructor.
        """
        print("Inside __init__()")
        self.f = f

    def __call__(self, *args):
        """
        The __call__ method is not called until the
        decorated function is called.
        """
        print("Inside __call__()")
        print("Function  arguments:", args)
        self.f(*args)
        print("After self.f(*args)")


class DecoratorClassWithArguments(object):

    def __init__(self, *dec_args):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        print("Inside __init__()")
        self.dec_args = dec_args

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        print("Inside __call__()")

        def wrapped_f(*args):
            print("Inside wrapped_f()")
            print("Decorator arguments:", self.dec_args)
            print("Function  arguments:", args)
            f(*args)
            print("After f(*args)")
        return wrapped_f


class DecoratorTestCase(base.ThinkingTestCase):

    def test_DecoratorFunctionWithArguments(self):

        @decoratorFunctionWithArguments("myarg", mykey='myvalue')
        def sayHello(a1, a2, a3, a4):
            print('Inside sayHello')
            print('sayHello arguments:', a1, a2, a3, a4)

        print("After decoration")

        print("Preparing to call sayHello()")
        sayHello("say", "hello", "argument", "list")

    def test_DecoratorClassWithoutArguments(self):
        print("Before decoration")

        @DecoratorClassWithoutArguments
        def sayHello(a1, a2, a3, a4):
            print('Inside sayHello')
            print('sayHello arguments:', a1, a2, a3, a4)

        print("After decoration")

        print("Preparing to call sayHello()")
        sayHello("say", "hello", "argument", "list")

    def test_DecoratorClassWithArguments(self):

        @DecoratorClassWithArguments("hello", "world", 42)
        def sayHello(a1, a2, a3, a4):
            print('Inside sayHello')
            print('sayHello arguments:', a1, a2, a3, a4)

        print("After decoration")

        print("Preparing to call sayHello()")
        sayHello("say", "hello", "argument", "list")

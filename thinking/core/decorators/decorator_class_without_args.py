# coding=utf-8
# http://blog.csdn.net/beckel/article/details/3945147
# function with decorator

from __future__ import print_function

import logging

from thinking.tests import base


LOG = logging.getLogger(__name__)


class DecoratorClassWithoutArgs(object):
    def __init__(self, func):
        """
        If there are no decorator arguments, the function
        to be decorated is passed to the constructor.
        """
        print('Inside decorator class __init__, func=', func)
        self.func = func

    def __call__(self, *args):
        """
        The __call__ method is not called until the
        decorated function is called.
        """
        print('Inside decorator class __init__, func args=', args)
        self.func(*args)

print("Start decoration")


@DecoratorClassWithoutArgs
def sayHello(a1, a2, a3, a4):
    print('Inside sayHello')
print("After decoration\n")

print("Start calling sayHello()")
sayHello("say", "hello", "argument", "list")
print("After calling sayHello()\n")

'''副作用: 函数 sayHello 变成了一个类对象 !'''
print("Side effects, method sayHello have been changed to:", sayHello)

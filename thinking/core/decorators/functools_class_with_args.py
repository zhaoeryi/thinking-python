# coding=utf-8
# http://blog.csdn.net/beckel/article/details/3945147
# function with decorator

from __future__ import print_function
import functools
import logging


LOG = logging.getLogger(__name__)


class DecoratorClassWithArgs(object):

    def __init__(self, *dec_args):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        print('Inside decorator class __init__, dec_args=', dec_args)
        self.dec_args = dec_args

    def __call__(self, func):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        print('Inside decorator class __call__, func=', func)

        @functools.wraps(func)
        def wrapped_f(*args):
            print('Inside wrapped_f, func args=', args)
            func(*args)
        return wrapped_f

print("Start decoration")


@DecoratorClassWithArgs("hello", "world", 42)
def sayHello(a1, a2, a3, a4):
    print('Inside sayHello')
print("After decoration\n")

print("Start calling sayHello()")
sayHello("say", "hello", "argument", "list")
print("After calling sayHello()\n")

'''函数 sayHello 的名字被保留为 wrapped_f !'''
print("Good effects of functools, method sayHello's name have been remained to:", sayHello.__name__)

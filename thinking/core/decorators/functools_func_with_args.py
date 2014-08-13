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

import functools
import logging


LOG = logging.getLogger(__name__)

'''
The return value of the decorator function must be a function used to wrap the function to be decorated.
That is, Python will take the returned function and call it at decoration time, passing the function to be decorated.
That's why we have three levels of functions; the inner one is the actual replacement function.

decorator函数的返回值必须是一个封装待decorated函数的函数
也就是说，Python会保存返回函数然后在decoration期间调用，并传递待decorated函数
这也是为何有三层函数的原因：里面那个函数才是被替换的
'''


# 当参数为*arg时，表示接受一个array；当参数为**arg时，表示接受一个dict
def decoratorFuncWithArgs(*dec_args, **dec_kwargs):
    print('Inside decorator, dec_args=', dec_args, ', dec_kwargs=', dec_kwargs)

    def wrap(func):
        print('Inside wrap, func=', func)

        @functools.wraps(func)
        def wrapped_f(*args):
            print('Inside wrapped_f, func args=', args)
            func(*args)
        return wrapped_f
    return wrap

print("Start decoration")


@decoratorFuncWithArgs("myarg", mykey='myvalue')
def sayHello(a1, a2, a3, a4):
    print('Inside sayHello')
print("After decoration\n")

print("Start calling sayHello()")
sayHello("say", "hello", "argument", "list")
print("After calling sayHello()\n")

'''函数 sayHello 的名字被保留为 wrapped_f !'''
print("Good effects of functools, method sayHello's name have been remained to:", sayHello.__name__)

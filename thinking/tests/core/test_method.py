from __future__ import print_function

from thinking.tests import base


class MyClass(object):

    @classmethod
    def cls_method(cls, *arg):
        instance = cls(arg)

        return instance


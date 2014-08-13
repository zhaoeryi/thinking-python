# coding=utf-8
from __future__ import print_function

from thinking.tests import base


class MyWithKlass(object):

    def __enter__(self):
        """When with MyWithKlass() is used, return self"""
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """End of 'with' statement.  We're done here."""

    def __del__(self):
        """Called when the instance is about to be destroyed. This is also called a destructor."""

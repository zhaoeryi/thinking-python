# coding=utf-8
from __future__ import print_function

from thinking.tests import base


class MyWithKlass(object):

    def __init__(self):
        print('Entering MyWithKlass.__init__, instance is about to be created')
        
    def __enter__(self):
        """When with MyWithKlass() is used, return self"""
        print('Entering MyWithKlass.__enter__, "with" statement is started')
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """End of 'with' statement.  We're done here."""
        print('Entering MyWithKlass.__exit__,  "with" statement is ended')

    def __del__(self):
        """Called when the instance is about to be destroyed. This is also called a destructor."""
        print('Entering MyWithKlass.__exit__, instance is about to be destroyed')
             
    def myfunc(self):
        print("Entering MyWithKlass.myfunc")   
         
class StatementTestCase(base.ThinkingTestCase):
    def test_statement_with(self):
        # http://effbot.org/zone/python-with-statement.htm
        with MyWithKlass() as instance:
            instance.myfunc()
        print("Ending testcase test_mywithklass")    

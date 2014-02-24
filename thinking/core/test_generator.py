# coding=utf-8
import _hacking
import itertools
import inspect

class MyIterKlass(object):
    
    def __iter__(self):
        # A class become Iterable if it has the __iter__ method defined.
        for i in [0, 1, 2]:
            yield i

class GeneratorTestCase(_hacking.HackingTestCase):
    def test_count_with_next(self):
        firstval = 99
        num = itertools.count(firstval)
        for i in [0, 1, 2]:
            iteration = num.next()
            self.assertEqual(iteration, firstval + i)
            print 'num.next()=', iteration
        
    def test_count_with_for(self):
        firstval = 99
        LIMIT = 10000
        for num in itertools.count(firstval):
            if num >= LIMIT:
                break        
        self.assertEqual(num, LIMIT)
        print "Final num is:", num

    def test_yield(self):
        def it_func():
            # 当执行到包含 yield 的表达式时, 函数it_func挂起, 并将 yield之后的表达式作为返回值 
            print 'entering func'
            print 'yield first time'
            yield 'first value'
            print 'yield second time'
            yield 'second value'
            print 'leaving func'

        it = it_func()
        print 'type of it is ', type(it)
        self.assertTrue(inspect.isgenerator(it))
        
        while True:
            try:
                # next()会触发 it_func 从上次断点继续执行, 直到再次遇到yield为止, 并接收到yield的返回值
                value = it.next()
                print "get return value=", value
            except StopIteration:
                print "catch StopIteration exception"
                return     

    def test_iter_object(self):
        rv = MyIterKlass()
        rv = list(rv)
        # iterate over instance of MyIterKlass now.
        for item in rv:
            print item

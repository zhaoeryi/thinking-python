import _hacking

class MyObj(object):
    def member_method(self, *arg):
        print "In member_method, input value is %s" % arg

def gobal_method(*args, **kwargs):
    print 
    
class MyClass(object):
    def __init__(self, *arg):
        print "in MyClass __init__ method, arg=", arg
        
    @classmethod
    def cls_method(cls, *arg):
        print "in MyClass classmethod, cls=", cls, ", arg=", arg
        instance = cls(arg)

        return instance
        
class MySubClass(MyClass):
    @staticmethod
    def static_method(*arg):
        print "in MySubClass static method, arg=", arg
               
class MethodTestCase(_hacking.HackingTestCase):
    def test_invoke_method_byattr(self):
        obj = MyObj()
        meth = getattr(obj, "member_method")
        # my_method function will be invoked!
        if callable(meth):
            meth(123456);
            
    def test_invoke_class_method(self):        
        MyClass.cls_method(123)
        print
        
        MyClass().cls_method(456)
        print
        
        MySubClass.cls_method(789)
      
    def test_invoke_static_method(self): 
        MySubClass.static_method(123)  
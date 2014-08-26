import eventlet

'''
$ python un-co-op.py 
main: i=0
main: i=1
main: i=2
foo(A): i=0
foo(A): i=1
foo(A): i=2
foo(B): i=0
foo(B): i=1
foo(B): i=2
'''

def foo(name):
    for i in range(3):
        print "foo(%s): i=%d" % (name, i)
    
f1 = eventlet.spawn(foo, 'A')
f2 = eventlet.spawn(foo, 'B')
 
for i in range(3):
    print "main: i=%d" % i
 
f1.wait()
f2.wait()
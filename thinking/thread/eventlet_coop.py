import eventlet
'''
$ python co-op.py 
func2
func1
'''

def func1():
    # suspend me and run something else 
    # but switch back to me after 2 seconds (if you can)
    eventlet.sleep(5)
    print "func1"
    
def func2():
    eventlet.sleep(1)
    print "func2"
    
f1 = eventlet.spawn(func1)
f2 = eventlet.spawn(func2)
 
f1.wait()
f2.wait()
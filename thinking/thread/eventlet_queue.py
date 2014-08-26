import eventlet
'''
$ python queue.py 
func1 hello
func2 world
'''

q = eventlet.Queue()
 
def func1():
    print "func1", q.get()
    
def func2():
    print "func2", q.get()
    
waiton = (eventlet.spawn(func1), eventlet.spawn(func2))
 
q.put("hello")
q.put("world")
 
for w in waiton:
    w.wait()
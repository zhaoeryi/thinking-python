import eventlet
'''
$ python spawn.py 
<eventlet.greenthread.GreenThread object at 0xe77870>
1 + 2 = 3
'''

def add(x, y):
    return x + y
    
e = eventlet.spawn(add, 1, 2)
print e
res = e.wait()
print '1 + 2 =', res
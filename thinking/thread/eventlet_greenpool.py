import eventlet
'''
$ python greenpool.py 
execute 1
execute 2
execute 3
1
2
execute 4
3
4
'''

pool = eventlet.GreenPool(size=2)

def printer(x):
    print x
    
print "execute 1"
pool.spawn(printer, 1)
print "execute 2"
pool.spawn(printer, 2)
print "execute 3"
pool.spawn(printer, 3)
print "execute 4"
pool.spawn(printer, 4)
 
pool.waitall()
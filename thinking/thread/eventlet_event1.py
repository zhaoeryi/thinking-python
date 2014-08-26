import eventlet
from eventlet import event
 
evt = event.Event()
 
def waiter():
    print "waiter: before wait()"
    evt.wait()
    print "waiter: after wait()"
    
w = eventlet.spawn(waiter)
 
print "main: before send()"
evt.send()
print "main: after send()"
 
w.wait()
print "main: at end"
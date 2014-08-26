import eventlet
import sys
from eventlet import event
 
evt = event.Event()

def waiter(num):
    print "waiter %d: before wait()" % num
    evt.wait()
    print "waiter %d: after wait()" % num

count = 0
while True:
    count = count + 1
    print count
    w = eventlet.spawn(waiter, count)
    eventlet.sleep(0)
   

print "main: before sleep()"
eventlet.sleep(10)
print "main: after sleep()"

print "main: before send()"
evt.send()
print "main: after send()"
 
w.wait()
print "main: at end"
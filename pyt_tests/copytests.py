# A quick python routine to display formating of Tracker.dump() for visual inspection

import gc
import copy
import pytracker as pyt
from StringIO import StringIO
import pickle

#gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS | gc.DEBUG_LEAK | gc.DEBUG_SAVEALL )

t = pyt.Tracker()
pyt.set_global_tracker(t)

class foo(pyt.Trackable):
    def __init__(self, msg):
        self.msg = "message is: " + str(msg)
        self._set_data_bundle( ('bundle', msg, str(self)) )

class foos(pyt.Trackable):
    __slots__ = ['msg']
    def __init__(self, msg):
        self.msg = "message is: " + str(msg)
        self._set_data_bundle( ('bundle', msg, str(self)) )

    def __getstate__(self):
        return (self.msg, super(foos, self).__getstate__())

    def __setstate__(self, arg):
        self.msg = arg[0]
        super(foos, self).__setstate__(arg[1])


t.set_object_tracking(foo)
t.set_object_tracking(foos)
t.set_object_tracking(pyt.Trackable)

def pickled(obj):
    buf = StringIO()
    pickle.dump(obj, buf, pickle.HIGHEST_PROTOCOL)
    return buf.getvalue()

def unpickle(buf):
    return pickle.load(StringIO(buf))

print "\nTesting normal derived object\n"

x = foo('foo object')
print "data bundle before: " + str(x._get_data_bundle())
print "foo before: " + str(x)
print "data bundle before: " + str(x._get_data_bundle())
print "msg before: " + x.msg
t.dump()
px = pickled(x)
x = None
t.dump()
x = unpickle(px)
y = copy.deepcopy(x)
print "foo after: " + str(x)
print "data bundle after: " + str(x._get_data_bundle())
print "msg after: " + x.msg
t.dump()
x = None
t.dump()
y = None
t.dump()

print "\nTesting bare trackable\n"

x = pyt.Trackable()
x._set_data_bundle('hardcoded bundle')
print "data bundle before: " + str(x._get_data_bundle())
print "bar before: " + str(x)
print "data bundle before: " + str(x._get_data_bundle())
t.dump()
px = pickled(x)
x = None
t.dump()
x = unpickle(px)
y = copy.deepcopy(x)
print "bar after: " + str(x)
print "data bundle after: " + str(x._get_data_bundle())
t.dump()
x = None
t.dump()
y = None
t.dump()

print "\nTesting subclass with slots\n"

x = foos('foos object')
print "data bundle before: " + str(x._get_data_bundle())
print "foos before: " + str(x)
print "data bundle before: " + str(x._get_data_bundle())
print "msg before: " + x.msg
t.dump()
px = pickled(x)
x = None
t.dump()
x = unpickle(px)
y = copy.deepcopy(x)
print "foos after: " + str(x)
print "data bundle after: " + str(x._get_data_bundle())
print "msg after: " + x.msg
t.dump()
x = None
t.dump()
y = None
t.dump()


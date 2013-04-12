# A quick python routine to display formating of Tracker.dump() for visual inspection

import pytracker as pyt

class foo1(pyt.Trackable):
    def __init__(self, msg):
        self._set_data_bundle(msg)

class foo2(foo1):
    pass

class foo3(foo1):
    _disable_global_tracker = True

t = pyt.Tracker()
pyt.set_global_tracker(t)

x1 = foo1('first')
x2 = foo2('second')
x3 = foo1('third')
x4 = foo2('fourth')
x5 = foo3('not to be tracked')

t.dump()

x3 = x4 = x5 = None

t.dump()

t.track_class(foo1)
t.track_class(foo2)

x1 = foo1('fifth')
x2 = foo2('sixth')
x3 = foo1('seventh')
x4 = foo2('eighth')

t.dump()

x1 = x2 = x3 = None

t.dump()

class TrackerMixin(object):

    def notify_attached(self, t):
        print "notify_attached: " + str(t)

    def notify_detached(self, t):
        print "notify_detached: " + str(t)

    def notify_destroyed(self, t):
        print "notify_destroyed: " + str(t)

class Tracker(TrackerMixin):
    pass


class TrackerMixin(object):

    def notify_attached(self, serial, obj_type, bundle):
        pass

    def notify_detached(self, serial, obj_type, bundle):
        pass

    def notify_destroyed(self, serial, obj_type, bundle):
        pass


class _TrackedType(object):
    objtype = None
    allocated = 0
    deallocated = 0

class Tracker(TrackerMixin, dict):

    def _get_entry(self, serial, objtype, bundle):
        name = objtype.__name__
        try:
            return self[name]
        except KeyError:
            pass
        e = self[name] = _TrackedType()
        e.objtype = objtype
        return e

    def notify_attached(self, *args):
        e = self._get_entry(*args)
        e.allocated += 1

    def notify_detached(self, *args):
        e = self._get_entry(*args)
        e.allocated -= 1

    def notify_destroyed(self, *args):
        e = self._get_entry(*args)
        e.allocated -= 1
        e.deallocated += 1

    def dump(self):
        for t in self.itervalues():
            print "%s\t\tallocated: %d, retired: %d" % (t.objtype.__name__, t.allocated, t.deallocated)

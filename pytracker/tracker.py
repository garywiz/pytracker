import copy

class TrackerMixin(object):

    def notify_attached(self, serial, obj_type, bundle):
        pass

    def notify_detached(self, serial, obj_type, bundle):
        pass

    def notify_destroyed(self, serial, obj_type, bundle):
        pass


class TrackedType(object):
    objtype = None
    allocated = 0
    deallocated = 0
    objects = None

    @property
    def track_objects(self):
        return self.objects is not None

    @track_objects.setter
    def track_objects(self, trackem):
        if self.objects is None:
            self.objects = dict()

    def track(self, serial, objtype, bundle):
        if self.objects is not None:
            self.objects[serial] = bundle

    def untrack(self, serial, objtype, bundle):
        if self.objects is not None:
            try:
                del self.objects[serial]
            except KeyError:
                pass
    
    def dump_objects(self):
        if self.objects:
            for s,o in self.objects.iteritems():
                print "   obj#{0:<8d} bundle:'{1}'".format(s, o or "")


class Tracker(TrackerMixin, dict):

    _dict_snapshot = None

    @staticmethod
    def format_changed_value(current, previous):
        if previous is None or current == previous:
            return str(current)
        return "{0} ({1:+d})".format(current, current - previous)
        
    def _get_entry(self, serial, objtype, bundle):
        name = objtype.__name__
        try:
            return self[name]
        except KeyError:
            pass
        e = self[name] = TrackedType()
        e.objtype = objtype
        return e

    def track_class(self, cls):
        self._get_entry(0, cls, None).track_objects = True

    def notify_attached(self, *args):
        e = self._get_entry(*args)
        e.track(*args)
        e.allocated += 1

    def notify_detached(self, *args):
        e = self._get_entry(*args)
        e.untrack(*args)
        e.allocated -= 1

    def notify_updated(self, *args):
        e = self._get_entry(*args)
        e.track(*args)

    def notify_destroyed(self, *args):
        e = self._get_entry(*args)
        e.untrack(*args)
        e.allocated -= 1
        e.deallocated += 1

    def dump(self):
        odict = self._dict_snapshot

        for t in self.itervalues():
            oldentry = odict and odict.get(t.objtype.__name__)
            print "{name:<40s} allocated: {alloc:<12s} retired: {dealloc:<12s}".format(
                name = t.objtype.__name__,
                alloc = self.format_changed_value(t.allocated, oldentry and oldentry.allocated), 
                dealloc = self.format_changed_value(t.deallocated, oldentry and oldentry.deallocated))
            t.dump_objects()

        self._dict_snapshot = {k:copy.copy(v) for k,v in self.iteritems()}


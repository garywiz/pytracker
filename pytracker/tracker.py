import copy

class TrackerMixin(object):

    """
    This class defines the protocol which must be supported by objects which are assigned
    to trackable objects using :py:meth:`Trackable._set_tracker` or :py:func:`pytracker.set_global_tracker`.

    Note that the :py:class:`pytracker.Trackable` class does not require that all of these
    methods be defined.  In fact, if they are not defined, there will be no error and the
    notification will not be sent.  As a rule, however, it is best to subclass the 
    :py:class:`~pytracker.TrackerMixin` class, as additional methods may be added in the future.

    """

    def notify_attached(self, serial, obj_type, bundle):
        """
        Whenever a trackable object is first assigned to a tracker, this method is triggered.

        :param serial: The unique serial number fo the trackable object.
        :param obj_type: The type of the object, essentially ``type(obj)``.
        :param bundle: The bundle object which may contain useful tracking information.
        """

    def notify_detached(self, serial, obj_type, bundle):
        """
        Just before a trackable object is assigned an alternate tracker (or ``None``) this method
        is triggered.

        :param serial: The unique serial number fo the trackable object.
        :param obj_type: The type of the object, essentially ``type(obj)``.
        :param bundle: The bundle object which may contain useful tracking information.
        """

    def notify_destroyed(self, serial, obj_type, bundle):
        """
        Just before a trackable object is freed, this method is triggered.

        :param serial: The unique serial number fo the trackable object.
        :param obj_type: The type of the object, essentially ``type(obj)``.
        :param bundle: The bundle object which may contain useful tracking information.
        """

    def notify_updated(self, serial, obj_type, bundle):
        """
        If the bundle associated with a trackable object is changed, this method is triggered.

        :param serial: The unique serial number fo the trackable object.
        :param obj_type: The type of the object, essentially ``type(obj)``.
        :param bundle: The bundle object which may contain useful tracking information.
        """

class TrackedType(object):
    """
    Internal class used to track a given object type.  May be subclassed and
    assigned to :py:attr:`pytracker.Tracker.type_tracker` to override the default
    implementation.
    """

    #: Contains the type of the tracked object
    objtype = None

    #: Contains the number of instances currently allocated for the type
    allocated = 0

    #: Contains the number of instances which have been deallocated
    deallocated = 0

    #: Contains an optional dictionary for tracking objects by serial number
    objects = None

    @property
    def track_objects(self):
        "Set to ``True`` to track objects individually.  Defaults to ``False``."
        return self.objects is not None

    @track_objects.setter
    def track_objects(self, trackem):
        if trackem:
            if self.objects is None:
                self.objects = dict()
        else:
            self.objects = None

    def track(self, serial, objtype, bundle):
        "Called by the tracker to register tracking for a given live object."
        if self.objects is not None:
            self.objects[serial] = bundle

    def untrack(self, serial, objtype, bundle):
        "Called by the tracker to indicate that an object is no longer live."
        if self.objects is not None:
            try:
                del self.objects[serial]
            except KeyError:
                pass
    
    def dump_objects(self, output = None):
        """
        Prints the status of all allocated objects for this type to ``stdout`` or
        an optional file object.
        """
        if self.objects:
            for s,o in self.objects.iteritems():
                print >>output, "   obj#{0:<8d} bundle:'{1}'".format(s, o or "")


class Tracker(TrackerMixin, dict):

    """
    This is a sample tracker object which can be used directly, or as a model for implementing
    custom tracker objects.
    """

    #: Class variable to specify the class used to track types
    type_tracker = TrackedType

    _dict_snapshot = None

    @staticmethod
    def _format_changed_value(current, previous):
        "Prints a value along with its delta."
        if previous is None or current == previous:
            return str(current)
        return "{0} ({1:+d})".format(current, current - previous)
        
    def _get_entry(self, serial, objtype, bundle):
        "Returns the object tracker for this entry."
        name = objtype.__name__
        try:
            return self[name]
        except KeyError:
            pass
        e = self[name] = self.type_tracker()
        e.objtype = objtype
        return e

    def set_object_tracking(self, cls, enable = True):
        """
        Enables tracking of objects for the given class.   If tracking is
        disabled, all object history is lost.
        """
        self._get_entry(0, cls, None).track_objects = enable

    def reset_object_tracking(self, cls):
        """
        Clears any tracked objects for the given class.  Does nothing if object
        tracking is not enabled for this class.
        """
        ent = self._get_entry(0, cls, None)
        if ent.track_objects:
            ent.track_objects = False
            ent.track_objects = True

    def notify_attached(self, *args):
        "Triggered whenever a new trackable object is created."
        e = self._get_entry(*args)
        e.track(*args)
        e.allocated += 1

    def notify_detached(self, *args):
        "Triggered whenver an existing trackable object is no longer being racked."
        e = self._get_entry(*args)
        e.untrack(*args)
        e.allocated -= 1

    def notify_updated(self, *args):
        "Triggered when the data bundle for a currently tracked object is changed."
        e = self._get_entry(*args)
        e.track(*args)

    def notify_destroyed(self, *args):
        "Triggered when an object being tracked is freed."
        e = self._get_entry(*args)
        e.untrack(*args)
        e.allocated -= 1
        e.deallocated += 1

    def dump(self, output = None):
        """
        Dumps the object tracking table to ``stdout`` or to the given file object.
        """

        odict = self._dict_snapshot

        for k in sorted(self.keys()):
            t = self[k]
            oldentry = odict and odict.get(t.objtype.__name__)
            print >>output, "{name:<40s} allocated: {alloc:<12s} retired: {dealloc:<12s}".format(
                name = t.objtype.__name__,
                alloc = self._format_changed_value(t.allocated, oldentry and oldentry.allocated), 
                dealloc = self._format_changed_value(t.deallocated, oldentry and oldentry.deallocated))
            t.dump_objects(output)

        self._dict_snapshot = {k:copy.copy(v) for k,v in self.iteritems()}


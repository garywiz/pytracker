.. pytracker documentation

Making Objects Trackable
========================

The :py:class:`pytracker.Trackable` class makes it easy to do production-level tracking of
object usage and allocation at runtime.

Unlike other memory profiling tools, trackable objects are intended to be incorporated
into the design of your system by becoming the superclass of objects which are important to track.
It is especially useful for long-running applications where it is often difficult to determine
where memory-leaks and bottlenecks are located until the application has been operating 
for longer periods of time in production.

Trackable objects have none of the limitations commonly associated with the :py:meth:`~object.__del__` method.
Objects destruction will occur normally and will be collected by Python's circular garbage
detector.  However, this means that trackable objects can be bent to insidious purposes such
as creating "hidden" destructors or observables.  Such uses, those possible, are not advised
due to the problems inherent in accessing an object during its destruction phase.

In most respects, you can substitute :py:class:`~pytracker.Trackable`
for any situation where :py:class:`object` is used, with the following
caveats:

* Just as with any built-in object, you cannot multiply inherit from
  both :py:class:`~pytracker.Trackable` and another built-in type
  (such as :py:class:`dict` or :py:class:`list`).  This is a
  limitation which applies to all Python built-ins, but means that it
  is not as simple as you'd like to create a trackable
  :py:class:`dict`, for example.
* Objects which inherit from :py:class:`~pytracker.Trackable` must be
  pickled with protocol level 2 or greater.

Aside from the above, there are few limitations, and almost no performance overhead in using
trackable objects.

Using trackable objects is relatively straightforward:

* Instrument your code by assuring that relevant classes have
  :py:class:`~pytracker.Trackable` as their superclass.
* Assign a tracker to each object created.  You can do this by using
  :py:meth:`~Trackable._set_tracker` to assign the tracker
  in :py:meth:`__init__`, but it is better to set a global tracker
  using :py:func:`pytracker.set_global_tracker`.  Using a global
  tracker allows you to track unpickled objects more easily.
* Use the :py:meth:`pytracker.Tracker.dump` method to display the current inventory of objects, organized
  by class.  It is up to you to decide when and how to dump tracking information.  For example
  in one application of ours, we intercept ``SIGUSR1`` and write tracking information to our
  standard log file.   You can write your own tracker, however, to accomplish a much wider
  variety of tasks.  Any class which supports the :py:class:`~pytracker.TrackerMixin` protocol can
  be assigned as an object tracker.  You can even create specialized trackers for different
  types of objects and use them concurrently.
  
pytracker.Trackable class
-------------------------

.. py:class:: pytracker.Trackable

   Any object to be tracked should be a subclass of this class.
   
.. py:method:: Trackable._set_tracker(tracker)

   Assign a tracker to this object.
   
   :param tracker: The new tracker object
   
   This method can be used to set, or change, the tracker assigned to
   an object.  When a new tracker is assigned, the tracker's
   :py:meth:`~pytracker.TrackerMixin.notify_attached` method will be
   triggered, notifying the tracker that a new object is being
   tracked.  If there was a tracker previously assigned (even if it
   was the same one), then the :py:meth:`~pytracker.TrackerMixin.notify_detached`
   method will be triggered for the old tracker beforehand.
   
   Because the current data bundle will be delivered with the notification, it is important to assure
   that the bundle is set before assigning a tracker if the tracker depends upon the bundle's value.
   
   You can remove the assigned tracker by setting the tracker to ``None``.
   
.. py:method:: Trackable._get_tracker() -> current tracker object or ``None``

   Returns the currently assigned tracker object, or ``None`` if no tracker has been assigned.
   Note that if a global tracker is assigned, this method will, as one would expect, return
   the value the global tracker had when the instance was first created or unpickled.
   
.. py:method:: Trackable._set_data_bundle(bundle)

   Set the object's data bundle.
   
   :param bundle: Any python object to be delivered to the tracker when an object is created, destroyed
                  or updated.

   The data bundle is an object that may be used by the tracker to
   maintain information about the pool of objects, such as extended
   information about the object, memory allocation information, or
   other debugging information.  The built-in
   :py:class:`pytracker.Tracker` object does not use the data bundle,
   so it is entirely optional to obtain basic tracking information for
   objects.
   
   .. note:: The data bundle should *not* contain a reference to the
      original object, no matter how tempting it is to do so.
      Including the original object, while possible, requires extreme
      caution since the
      :py:meth:`~pytracker.TrackerMixin.notify_destroyed` trigger
      method is called when the tracked object is being deallocated.
      While it is acceptable to access the object at this time, it is
      essential that no references be kept, otherwise unpredictable
      behavior may result.

      For this reason, the serial number should be used to create tracking information or data
      about the object, if indeed individual object tracking is desired.

      When the bundle is set, the tracker's
      :py:meth:`~pytracker.TrackerMixin.notify_updated` is triggered.
   
.. py:method:: Trackable._get_data_bundle() -> current data bundle object

   This method returns the currently set data bundle object associated with this object.
   
.. py:method:: Trackable._get_tracker_serial() -> unique integer serial number

   When it is created, each trackable object is assigned a unique, monotonically increasing serial
   number.  

Pickling and Copying
--------------------

For the most part, instances :py:class:`~pytracker.Trackable` object subclasses may be
copied and pickled using any normal means, such as :py:func:`copy.copy` or :py:func:`pickle.dumps`.

By default, trackable objects conform to the protocol 2 :py:meth:`~object.__setstate__` and
:py:meth:`~object.__getstate__` implementations as described in :pep:`307`.  In other words,
``__getstate__`` is expected to return a tuple::

   (dict_or_none, slot_state_dict_or_none)

Generally, subclasses which want to deliver a custom state should either override 
``__getstate__`` completely, or call the superclass ``__getstate__`` and modify its contents
before returning it.


Module Functions
----------------

.. py:function:: pytracker.set_global_tracker(tracker)

   Specifies a global tracker to be used when any trackable object is created.

   :param tracker: Any object which conforms to the :py:class:`pytracker.TrackerMixin` protocol.

.. py:function:: pytracker.version() -> version string

   Returns the version of the trackable objects module.  Currently returns an integer value ``1``.

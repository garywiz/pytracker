import unittest
import gc
import pytracker as pyt

class track1(pyt.Trackable):

    def __init__(self, t):
        self._set_data_bundle('bundle one')
        self._set_tracker(t)

class track2(pyt.Trackable):

    def __init__(self, t):
        self._set_data_bundle('bundle two')
        self._set_tracker(t)

class SerialTracker(pyt.Tracker):

    def _get_entry(self, serial, objtype, bundle):
        try:
            return self[serial]
        except KeyError:
            pass
        e = self[serial] = pyt.tracker._TrackedType()
        e.objtype = objtype
        e.bundle = bundle
        return e
    
class test_all(unittest.TestCase):

    def test_version(self):
        self.assertEqual(pyt.version(), 1, 'Incorrect pytracker version number.')

    def test_trackable1(self):
        "Assure basic tracking works properly."
        tracker = pyt.Tracker()
        obj = track1(tracker)
        self.assertEqual(len(tracker), 1)
        self.assertEqual(tracker.values()[0].allocated, 1)
        self.assertEqual(tracker.keys()[0], 'track1')
        obj = None
        gc.collect()
        self.assertEqual(tracker.values()[0].deallocated, 1)

    def test_trackable2(self):
        "Assure both objects are tracked as allocated and deallocated."
        tracker = pyt.Tracker()
        obj1 = track1(tracker)
        obj2 = track2(tracker)
        self.assertEqual(len(tracker), 2)
        self.assertEqual(tracker['track1'].allocated, 1)
        self.assertEqual(tracker['track2'].allocated, 1)
        obj1 = obj2 = None
        gc.collect()
        self.assertEqual(tracker['track1'].allocated, 0)
        self.assertEqual(tracker['track2'].allocated, 0)

    def test_trackable3(self):
        "Check whether serial number and bundle tracking work."
        tracker = SerialTracker()
        obj1 = track1(tracker)
        obj2 = track2(tracker)
        obj3 = track1(tracker)
        obj4 = track2(tracker)
        self.assertEqual(len(tracker), 4)
        obj1s = obj1._get_tracker_serial()
        obj2s = obj2._get_tracker_serial()
        obj3s = obj3._get_tracker_serial()
        obj4s = obj4._get_tracker_serial()
        self.assertEqual(tracker[obj1s].allocated, 1)
        obj1 = obj2 = obj3 = obj4 = None
        gc.collect()
        self.assertEqual(tracker[obj1s].deallocated, 1)
        self.assertEqual(tracker[obj2s].deallocated, 1)
        self.assertEqual(tracker[obj3s].deallocated, 1)
        self.assertEqual(tracker[obj4s].deallocated, 1)
        self.assertEqual(tracker[obj1s].bundle, 'bundle one')
        self.assertEqual(tracker[obj3s].bundle, 'bundle one')
        self.assertEqual(tracker[obj2s].bundle, 'bundle two')
        self.assertEqual(tracker[obj4s].bundle, 'bundle two')

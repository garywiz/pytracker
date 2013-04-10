import unittest
import pytracker as pyt

class test_all(unittest.TestCase):

    def test_version(self):
        self.assertEqual(pyt.version(), 1, 'Incorrect pytracker version number.')

    def test_trackable1(self):
        obj = pyt.Trackable()
        print obj

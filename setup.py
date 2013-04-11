from setuptools import setup, Extension

trackable = Extension('pytracker.trackable',
                      sources = ['pytracker/trackable.c'])

setup(
    name = "pytracker",
    version = '1.0',
    description = 'Creates trackable objects for memory inventory purposes',
    ext_modules = [trackable],
    py_modules = ['pytracker/tracker', 'pytracker/__init__'],
    test_suite = "pyt_tests.tests.test_all",
    )

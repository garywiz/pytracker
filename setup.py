from setuptools import setup, Extension

pytracker = Extension('pytracker',
                      sources = ['pytracker.c', 'trackable.c'])

setup(
    name = "pytracker",
    version = '1.0',
    description = 'Creates trackable objects for memory inventory purposes',
    ext_modules = [pytracker],
    test_suite = "pyt_tests.tests.test_all",
    )

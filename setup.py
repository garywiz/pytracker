from setuptools import setup, Extension

trackable = Extension('pytracker.trackable',
                      sources = ['pytracker/trackable.c'])

readme = """pytracker is a simple python extension that allows you to track instance usage in 
production-level environments.

================   =====================================
Documentation      http://garywiz.github.io/pytracker
pytracker Source   http://github.com/garywiz/pytracker
pypi link          http://pypi.python.org/pypi/pytracker
================   =====================================
"""

setup(
    name = "pytracker",
    version = '1.0.3',          # ALSO update version number in pytracker/trackable.c & pyt_tests/tests.py
    description = 'Object tracking classes for efficient inventory of allocated/freed objects',
    long_description = readme,
    ext_modules = [trackable],
    py_modules = ['pytracker/tracker', 'pytracker/__init__'],
    test_suite = "pyt_tests.tests.test_all",
    license = "BSD 3",
    author = "Gary Wisniewski",
    author_email = "pypi-garywiz@gw.spidereye.com",
    url = "http://github.com/garywiz/pytracker",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: C",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: System :: Monitoring",
        ]
    )

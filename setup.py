from setuptools import setup, Extension

trackable = Extension('pytracker.trackable',
                      sources = ['pytracker/trackable.c'])

with open('README.pypi') as file:
    long_description = file.read()

setup(
    name = "pytracker",
    version = '1.0',
    description = 'Object tracking classes for efficient inventory of allocated/freed objects',
    long_description = long_description,
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

.. pytracker documentation master file, created by
   sphinx-quickstart on Mon May  6 17:19:12 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pytracker: Built-in Object Tracking for Production Code
=======================================================

The ``pytracker`` extension provides a small, efficient set of classes
for tracking object usage in production code.  In order to track objects,
they must be subclasses of the :py:class:`pytracker.Trackable` class, which
in most cases behaves exactly like the :py:class:`object` class.

Unlike existing packages like
`Heapy <http://guppy-pe.sourceforge.net/>`_ and
`PySizer <http://pysizer.8325.org/>`_, ``pytracker`` is not designed for
profiling or debugging existing code, but is rather designed to allow
you instrument production systems for monitoring of object usage
during normal operation.  It is especially useful for optimizing long-running
systems which may exhibit memory leaks or unusual usage patterns over time.

Though you can create your own tracker to collect more comprehensive information
about live objects, there is a simple tracker provided which can be used quickly
and easily.  For example::

    >>> from pytracker import Tracker, Trackable, set_global_tracker
    >>> t = Tracker()
    >>> set_global_tracker(t)
    >>> 
    >>> class track_my_instances(Trackable):
    ...   pass
    ... 
    >>> i1 = track_my_instances()
    >>> i2 = track_my_instances()
    >>> t.dump()
    track_my_instances                       allocated: 2            retired: 0           
    >>> i1 = None
    >>> t.dump()
    track_my_instances                       allocated: 1 (-1)       retired: 1 (+1)      
    >>> 

Tracked objects must be pickled using a protocol level of 2 or greater when
using :py:func:`pickle.dump`.

Any bugs should be reported as issues at https://github.com/garywiz/pytracker/issues.

Contents
--------

.. toctree::
   :maxdepth: 2

   pytracker.trackable
   pytracker.tracker

Downloading and Installing
--------------------------

The easiest way to install ``pytracker`` is using ``pip`` from the https://pypi.python.org/pypi/pytracker package::

    # Ubuntu or debian prerequisites...
    apt-get install pip
    apt-get install python-dev
    apt-get install gcc

    # pytracker installation (may be all you need)
    pip install pytracker

If you're interested in the source code, or contributing, you can find the ``pytracker`` source code 
at https://github.com/garywiz/pytracker.
    
Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License
-------

This software is distributed under the `BSD-3 License <http://opensource.org/licenses/BSD-3-Clause>`_:

Copyright (c) 2013, Gary J. Wisniewski,
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer:

   Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the
   distribution.  Neither the name of the author, the author's
   organization, nor the names of its contributors may be used to
   endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

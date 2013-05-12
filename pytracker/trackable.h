#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    PyObject *tracker;		/* the tracker object */
    PyObject *data_bundle;	/* a data bundle for general purpose use */
    PyObject *serial;		/* unique serial number of this object */
    PyObject *weakreflist;	/* the requisite weakref list */
} Trackable;

extern PyTypeObject _TrackableType;

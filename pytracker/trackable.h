#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    PyObject *tracker;
    PyObject *data_bundle;
    PyObject *serial;
} Trackable;

extern PyTypeObject _TrackableType;

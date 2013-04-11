#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    PyObject *tracker;
} Trackable;

extern PyTypeObject _TrackableType;

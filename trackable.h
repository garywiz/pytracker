#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
} Trackable;

extern PyTypeObject _TrackableType;

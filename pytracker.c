#include "pytracker.h"

PyTypeObject * TrackableType = NULL;

static PyObject * pytracker_version(PyObject *self, PyObject *args)
{
    return Py_BuildValue("i", 1);
}

static PyMethodDef pytrackerMethods[] = {
    {"version", pytracker_version, METH_VARARGS,
     "Display version of pytracker extension"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initpytracker(void)
{
    PyObject *m;
    PyObject *PytrackerError;

    m = Py_InitModule("pytracker", pytrackerMethods);
    if (m == NULL)
	return;

    PytrackerError = PyErr_NewException("pytracker.error", NULL, NULL);
    Py_INCREF(PytrackerError);
    PyModule_AddObject(m, "error", PytrackerError);

    if (PyType_Ready(&_TrackableType) < 0)
	return;

    TrackableType = &_TrackableType;
    Py_INCREF(TrackableType);
    PyModule_AddObject(m, "Trackable", (PyObject*) TrackableType);
}

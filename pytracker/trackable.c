#include "trackable.h"

#define PING_ATTACH "notify_attached"
#define PING_DETACH "notify_detached"
#define PING_DESTROY "notify_destroyed"

static void pingtracker(Trackable *self, const char * method)
{
    PyObject * result;

    if (self->tracker == Py_None)
	return;
   
    result = PyObject_CallMethod(self->tracker, (char *)method, NULL);
    if (result == NULL) {
	PyErr_Clear();
    } else {
	Py_DECREF(result);
    }
}

PyObject* Trackable_new(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    Trackable* self = NULL;

    self = (Trackable*) type->tp_alloc(type, 0);
    if (self == NULL) goto error;

    self->tracker = Py_None;
    Py_INCREF(self->tracker);

    goto success;

error:
    Py_XDECREF(self);
    self = NULL;

success:
    return (PyObject*) self;
}

int Trackable_init(Trackable* self, PyObject* args, PyObject* kwargs)
{
    return 0;
}

static int Trackable_traverse(Trackable *self, visitproc visit, void *arg)
{
    Py_VISIT(self->tracker);

    return 0;
}

static int Trackable_clear(Trackable *self)
{
    Py_CLEAR(self->tracker);

    return 0;
}

void Trackable_dealloc(Trackable* self)
{
    pingtracker(self, PING_DESTROY);

    Trackable_clear(self);
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject * Trackable_get_tracker(Trackable *self)
{
    Py_INCREF(self->tracker);
    return self->tracker;
}

static PyObject * Trackable_set_tracker(Trackable *self, PyObject *arg)
{
    pingtracker(self, PING_DETACH);

    Py_XDECREF(self->tracker);
    Py_INCREF(arg);
    self->tracker = arg;

    pingtracker(self, PING_ATTACH);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMemberDef Trackable_members[] = {
    {NULL}
};

static PyMethodDef Trackable_methods[] = {
    {"set_tracker", (PyCFunction) Trackable_set_tracker, METH_O,
     "Set a new tracker object"
    },
    {"get_tracker", (PyCFunction) Trackable_get_tracker, METH_NOARGS,
     "Return the current tracker object"
    },
    {NULL}
};

PyTypeObject _TrackableType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "pytracker.trackable.Trackable", /*tp_name*/
    sizeof(Trackable),		/*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)Trackable_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC, /*tp_flags*/
    "Trackable Objects",       /* tp_doc */
    (traverseproc)Trackable_traverse, /*tp_traverse*/
    (inquiry)Trackable_clear,	      /*tp_clear*/
    0,			       /*tp_richcompare*/
    0,			       /*tp_weaklistoffset*/
    0,			       /*tp_iter*/
    0,			       /*tp_iternext*/
    Trackable_methods,	       /*tp_methods*/
    Trackable_members,	       /*tp_members*/
    0,			       /*tp_getset*/
    0,			       /*tp_base*/
    0,			       /*tp_dict*/
    0,			       /*tp_descr_get*/
    0,			       /*tp_descr_set*/
    0,			       /*tp_dictoffset*/
    (initproc)Trackable_init,  /*tp_init*/
    0,			       /*tp_alloc*/
    Trackable_new,	       /*tp_new*/
};

PyTypeObject * TrackableType = NULL;

static PyObject * trackable_version(PyObject *self, PyObject *args)
{
    return Py_BuildValue("i", 1);
}

static PyMethodDef trackableMethods[] = {
    {"version", trackable_version, METH_VARARGS,
     "Display version of pytracker extension"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC inittrackable(void)
{
    PyObject *m;
    PyObject *TrackableError;

    m = Py_InitModule("trackable", trackableMethods);
    if (m == NULL)
	return;

    TrackableError = PyErr_NewException("trackable.error", NULL, NULL);
    Py_INCREF(TrackableError);
    PyModule_AddObject(m, "error", TrackableError);

    if (PyType_Ready(&_TrackableType) < 0)
	return;

    TrackableType = &_TrackableType;
    Py_INCREF(TrackableType);
    PyModule_AddObject(m, "Trackable", (PyObject*) TrackableType);
}

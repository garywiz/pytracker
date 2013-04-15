#include "trackable.h"

static PyObject * meth_ATTACH;
static PyObject * meth_DETACH;
static PyObject * meth_DESTROY;
static PyObject * meth_UPDATE;

static PyObject *  global_tracker = NULL;
static unsigned long long serial_number = 0;

static void pingtracker(Trackable *self, PyObject * method)
{
    PyObject * result;

    if (self->tracker == Py_None)
	return;
   
    result = PyObject_CallMethodObjArgs(self->tracker, method, self->serial, self->ob_type, self->data_bundle, NULL);
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

    Py_INCREF(Py_None);
    self->data_bundle = Py_None;

    if (global_tracker != NULL && !PyObject_HasAttrString((PyObject*)type, "_disable_global_tracker"))
	self->tracker = global_tracker;
    else
	self->tracker = Py_None;

    Py_INCREF(self->tracker);

    self->serial = PyLong_FromUnsignedLongLong(++serial_number);

    pingtracker(self, meth_ATTACH);

    goto success;

error:
    Py_XDECREF(self);
    self = NULL;

success:
    return (PyObject*) self;
}

static int Trackable_traverse(Trackable *self, visitproc visit, void *arg)
{
    Py_VISIT(self->tracker);
    Py_VISIT(self->data_bundle);

    return 0;
}

static int Trackable_clear(Trackable *self)
{
    pingtracker(self, meth_DESTROY);

    Py_CLEAR(self->tracker);
    Py_CLEAR(self->serial);
    Py_CLEAR(self->data_bundle);

    return 0;
}

void Trackable_dealloc(Trackable* self)
{
    PyObject_GC_UnTrack(self);

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
    pingtracker(self, meth_DETACH);

    Py_XDECREF(self->tracker);
    Py_INCREF(arg);
    self->tracker = arg;

    pingtracker(self, meth_ATTACH);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject * Trackable_get_tracker_serial(Trackable *self)
{
    Py_INCREF(self->serial);
    return self->serial;
}

static PyObject * Trackable_get_data_bundle(Trackable *self)
{
    Py_INCREF(self->data_bundle);
    return self->data_bundle;
}

static PyObject * Trackable_set_data_bundle(Trackable *self, PyObject *arg)
{
    Py_XDECREF(self->data_bundle);
    Py_INCREF(arg);
    self->data_bundle = arg;

    pingtracker(self, meth_UPDATE);

    Py_RETURN_NONE;
}

static PyMemberDef Trackable_members[] = {
    {NULL}
};

static PyMethodDef Trackable_methods[] = {
    {"_set_tracker", (PyCFunction) Trackable_set_tracker, METH_O,
     "Set a new tracker object"
    },
    {"_get_tracker", (PyCFunction) Trackable_get_tracker, METH_NOARGS,
     "Return the current tracker object"
    },
    {"_set_data_bundle", (PyCFunction) Trackable_set_data_bundle, METH_O,
     "Set the optional data bundle for a trackable object"
    },
    {"_get_data_bundle", (PyCFunction) Trackable_get_data_bundle, METH_NOARGS,
     "Return the optional data bundle for a trackable object"
    },
    {"_get_tracker_serial", (PyCFunction) Trackable_get_tracker_serial, METH_NOARGS,
     "Return the unique serial number assigned to this object"
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
    0,			       /*tp_init*/
    0,			       /*tp_alloc*/
    Trackable_new,	       /*tp_new*/
};

PyTypeObject * TrackableType = NULL;

static PyObject * trackable_version(PyObject *self, PyObject *args)
{
    return Py_BuildValue("i", 1);
}

static PyObject * trackable_set_global_tracker(PyObject *self, PyObject *arg)
{
    Py_XDECREF(global_tracker);
    Py_INCREF(arg);
    global_tracker = arg;

    Py_RETURN_NONE;
}

static PyMethodDef trackableMethods[] = {
    {"version", trackable_version, METH_VARARGS,
     "Display version of pytracker extension"},
    {"set_global_tracker", trackable_set_global_tracker, METH_O,
     "Set the tracker to be used for all objects"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC inittrackable(void)
{
    PyObject *m;
    PyObject *TrackableError;

    m = Py_InitModule("trackable", trackableMethods);
    if (m == NULL)
	return;

    meth_ATTACH = Py_BuildValue("s", "notify_attached");
    meth_DETACH = Py_BuildValue("s", "notify_detached");
    meth_DESTROY = Py_BuildValue("s", "notify_destroyed");
    meth_UPDATE = Py_BuildValue("s", "notify_updated");

    TrackableError = PyErr_NewException("trackable.error", NULL, NULL);
    Py_INCREF(TrackableError);
    PyModule_AddObject(m, "error", TrackableError);

    if (PyType_Ready(&_TrackableType) < 0)
	return;

    TrackableType = &_TrackableType;
    Py_INCREF(TrackableType);
    PyModule_AddObject(m, "Trackable", (PyObject*) TrackableType);
}

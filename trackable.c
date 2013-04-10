#include "pytracker.h"

PyObject* Trackable_new(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    Trackable* self = NULL;

    self = (Trackable*) type->tp_alloc(type, 0);
    if(self == NULL) goto error;

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

void Trackable_dealloc(Trackable* self)
{
}

static PyMemberDef Trackable_members[] = {
    {NULL}
};

static PyMethodDef Trackable_methods[] = {
    {NULL}
};

PyTypeObject _TrackableType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "pytracker.Trackable",      /*tp_name*/
    sizeof(Trackable),		/*tp_basicsize*/
    0,                         /*tp_itemsize*/
    0,                         /*tp_dealloc*/
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
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "Trackable objects",       /* tp_doc */
    0,		               /*tp_traverse*/
    0,			       /*tp_clear*/
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

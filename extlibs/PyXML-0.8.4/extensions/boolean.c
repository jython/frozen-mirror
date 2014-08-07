/*
 Boolean extension, by Uche Ogbuji
 Copyright (c) 2001 Fourthought, Inc. USA.   All Rights Reserved.
 See  http://4suite.org/COPYRIGHT  for license and copyright information
*/

#include "Python.h"
#include <string.h>
#include <ctype.h>
#include <stdio.h>


#if defined(_WIN32) || defined(__WIN32__)
#include <float.h>
#define NaN_Check(x) _isnan(x)
#define Inf_Check(x) (_finite(x) && !_isnan(x))
#else
#include <math.h>
#define NaN_Check(x) isnan(x)
#define Inf_Check(x) isinf(x)
#endif

#define Boolean_Check(v)  ((v)->ob_type == &PyBoolean_Type)
#define Boolean_Value(v)  (((PyBooleanObject *)(v))->value)

typedef struct {
    PyObject_HEAD
    int value;
} PyBooleanObject;

static PyBooleanObject *g_true;
static PyBooleanObject *g_false;

static PyObject *g_true_string;
static PyObject *g_false_string;

static PyTypeObject PyBoolean_Type;


static PyObject *
BooleanValue(PyObject *self, PyObject *args) {
    PyObject *obj;
    PyObject *str_func;
    PyBooleanObject *result = NULL;

    if (!PyArg_ParseTuple(args, "O|O:BooleanValue", &obj, &str_func))
        return NULL;

    if (Boolean_Check(obj)){
        result = (PyBooleanObject *)obj;
    }
    else if (PyFloat_Check(obj)) {
        if (NaN_Check(PyFloat_AS_DOUBLE(obj))) {
            result = g_false;
        }
        else {
            result = PyObject_IsTrue(obj) ? g_true : g_false;
        }
    }
    else if (PyNumber_Check(obj) || PySequence_Check(obj)){
        result = PyObject_IsTrue(obj) ? g_true : g_false;
    }
    else if (str_func) {
        obj = PyObject_CallFunction(str_func, "(O)", obj);
        if (!obj)
            return NULL;
        result = PyObject_IsTrue(obj) ? g_true : g_false;
        Py_DECREF(obj);
    }
    else {
        result = g_false;
    }
    Py_INCREF(result);
    return (PyObject *)result;
}

static int
pyobj_as_boolean_int(PyObject *obj) {
    if (Boolean_Check(obj))
        return Boolean_Value((PyBooleanObject *)obj);
    else if (PyNumber_Check(obj) || PySequence_Check(obj))
        return PyObject_IsTrue(obj) ? 1 : 0;
    else
        return 0;
}

static PyObject *
IsBooleanType(PyObject *self, PyObject *args) {
    PyObject *obj;
    PyObject *result = NULL;

    if (!PyArg_ParseTuple(args, "O:IsBooleanType", &obj))
        return NULL;

    if (Boolean_Check(obj))
        result = Py_True;
    else
        result = Py_False;
    Py_INCREF(result);
    return result;
}

static PyBooleanObject *
boolean_NEW(int initval)
{
  PyBooleanObject *object = PyObject_NEW(PyBooleanObject, &PyBoolean_Type);
  object->value = initval;
  return object;
}

static void
boolean_dealloc(PyObject *self)
{
  PyMem_DEL(self);
}

static int
boolean_cmp(PyObject *o1, PyObject *o2){
    int result = -1;
    PyBooleanObject *b1;
    PyBooleanObject *b2;

    if (Boolean_Check(o1) && Boolean_Check(o2)) {
        b1 = (PyBooleanObject *)o1;
        b2 = (PyBooleanObject *)o2;
        result = !(Boolean_Value(o1) == Boolean_Value(o2));
    }
    else if (Boolean_Check(o1)) {
        b1 = (PyBooleanObject *)o1;
        result = !(Boolean_Value(o1) == pyobj_as_boolean_int(o2));
    }
    else if (Boolean_Check(o2)) {
        b2 = (PyBooleanObject *)o2;
        result = !(Boolean_Value(o2) == pyobj_as_boolean_int(o1));
    }
    return result;
}

static PyObject *
boolean_repr(PyObject *self)
{
    PyObject *result;

    if (Boolean_Value((PyBooleanObject *)self))
        result = g_true_string;
    else
        result = g_false_string;
    Py_INCREF(result);
    return result;
}

static int
boolean_coerce(PyObject **v, PyObject **w)
{
    PyObject *newv, *neww;

    if ((*v)->ob_type == (*w)->ob_type){
        Py_INCREF(*v);
        Py_INCREF(*w);
        return 0;
    }
    newv = PyNumber_Int(*v);
    neww = PyNumber_Int(*w);
    if (newv && neww){
        *v = newv;
        *w = neww;
        return 0;
    }
    Py_XDECREF(newv);
    Py_XDECREF(neww);
    return -1;  /* couldn't do it */
}

static PyObject *
boolean_and(PyObject *o1, PyObject *o2)
{
    /* FIXME: Check whether we need to conver the 1st arg.
       The Python/C docs don't help */
    int lhs = pyobj_as_boolean_int(o1), rhs = pyobj_as_boolean_int(o2);
    PyObject *result = NULL;

    result = PyInt_FromLong((long)(lhs && rhs));
    Py_INCREF(result);
    return result;
}

static PyObject *
boolean_or(PyObject *o1, PyObject *o2)
{
    /* FIXME: Check whether we need to conver the 1st arg.
       The Python/C docs don't help */
    int lhs = pyobj_as_boolean_int(o1), rhs = pyobj_as_boolean_int(o2);

    return PyInt_FromLong((long)(lhs || rhs));
}

static PyObject *
boolean_xor(PyObject *o1, PyObject *o2)
{
    /* FIXME: Check whether we need to conver the 1st arg.
       The Python/C docs don't help */
    int lhs = pyobj_as_boolean_int(o1), rhs = pyobj_as_boolean_int(o2);

    return PyInt_FromLong((long)(lhs ^ rhs));
}

static int
boolean_nonzero(PyObject *o)
{
    return Boolean_Value((PyBooleanObject *)o);
}

static PyObject *
boolean_int(PyObject *o)
{
    PyBooleanObject *obj = (PyBooleanObject *)o;

    return PyInt_FromLong((long)Boolean_Value(obj));
}

static PyObject *
boolean_long(PyObject *o)
{
    PyBooleanObject *obj = (PyBooleanObject *)o;

    return PyLong_FromLong((long)Boolean_Value(obj));
}

static PyObject *
boolean_float(PyObject *o)
{
    PyBooleanObject *obj = (PyBooleanObject *)o;

    return PyFloat_FromDouble((double)Boolean_Value(obj));
}

static PyNumberMethods boolean_as_number = {
    0,                 /* binaryfunc nb_add;       __add__ */
    0,                 /* binaryfunc nb_subtract;  __sub__ */
    0,                 /* binaryfunc nb_multiply;  __mul__ */
    0,                 /* binaryfunc nb_divide;    __div__ */
    0,                 /* binaryfunc nb_remainder; __mod__ */
    0,                 /* binaryfunc nb_divmod;    __divmod__ */
    0,                 /* ternaryfunc nb_power;    __pow__ */
    0,                 /* unaryfunc nb_negative;   __neg__ */
    0,                 /* unaryfunc nb_positive;   __pos__ */
    0,                 /* unaryfunc nb_absolute;   __abs__ */
    boolean_nonzero,   /* inquiry nb_nonzero;      __nonzero__ */
    0,                 /* unaryfunc nb_invert;     __invert__ */
    0,                 /* binaryfunc nb_lshift;    __lshift__ */
    0,                 /* binaryfunc nb_rshift;    __rshift__ */
    boolean_and,       /* binaryfunc nb_and;       __and__ */
    boolean_xor,       /* binaryfunc nb_xor;       __xor__ */
    boolean_or,        /* binaryfunc nb_or;        __or__ */
    boolean_coerce,    /* coercion nb_coerce;      __coerce__ */
    boolean_int,       /* unaryfunc nb_int;        __int__ */
    boolean_long,      /* unaryfunc nb_long;       __long__ */
    boolean_float,     /* unaryfunc nb_float;      __float__ */
    0,                 /* unaryfunc nb_oct;        __oct__ */
    0,                 /* unaryfunc nb_hex;        __hex__ */
};

static PyTypeObject PyBoolean_Type = {
    PyObject_HEAD_INIT(0)
    0,
    "boolean",
    sizeof(PyBooleanObject),
    0,
    boolean_dealloc,      /* tp_dealloc */
    0,                    /* tp_print */
    0,                    /* tp_getattr */
    0,                    /* tp_setattr */
    (cmpfunc)boolean_cmp, /* tp_compare */
    boolean_repr,         /* tp_repr */
    &boolean_as_number,   /* tp_as_number */
    0,                    /* tp_as_sequence */
    0,                    /* tp_as_mapping */
    0,                    /* tp_hash */
    0,                    /* tp_call */
    0,                    /* tp_str */
    0,                    /* tp_getattro */
    0,                    /* tp_setattro */
};

static PyMethodDef booleanMethods[] = {
     { "BooleanValue",  BooleanValue,  METH_VARARGS },
     { "IsBooleanType", IsBooleanType, METH_VARARGS },
     { NULL, NULL }
};

DL_EXPORT(void)
initboolean(void) {
  PyObject *m;

  m = Py_InitModule("boolean", booleanMethods);

  PyBoolean_Type.ob_type = &PyType_Type;
  Py_INCREF(&PyBoolean_Type);
  PyModule_AddObject(m, "BooleanType", (PyObject *)&PyBoolean_Type);

  if (g_true_string == NULL)
      g_true_string = PyString_FromString("true");
  if (g_false_string == NULL)
      g_false_string = PyString_FromString("false");

  if (g_true == NULL)
      g_true = boolean_NEW(1);
  if (g_false == NULL)
      g_false = boolean_NEW(0);

  Py_INCREF(g_true);
  PyModule_AddObject(m, "true", (PyObject *)g_true);
  Py_INCREF(g_false);
  PyModule_AddObject(m, "false", (PyObject *)g_false);

  return;
}
